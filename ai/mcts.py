import math
import numpy as np
import torch
import copy
from typing import List, Dict, Tuple, Optional

# Move imports to top to avoid overhead in loops
from .actions import Action
from .game_wrapper import HearthstoneGame

class MCTSNode:
    def __init__(self, state, parent=None, action_idx=None, action_obj=None):
        self.state = state
        self.parent = parent
        self.action_idx = action_idx
        self.action_obj = action_obj # Store full action object with simulator metadata
        
        self.children = {} # Map action_idx -> MCTSNode
        self.is_expanded = False
        
        self.visit_count = 0
        self.value_sum = 0.0
        self.prior_prob = 0.0 # From Policy Head
        
    @property
    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

class MCTS:
    """
    Monte Carlo Tree Search implementation guided by Neural Network.
    """
    
    def __init__(self, model, encoder, game_env, c_puct=1.0, num_simulations=50):
        self.model = model
        self.encoder = encoder
        self.game_env = game_env # Reference for cloning
        self.c_puct = c_puct
        self.num_simulations = num_simulations
        
        # Pre-instantiate a wrapper to reuse for logic checks (avoids repeated DB loads)
        self._temp_wrapper = HearthstoneGame()
        
    def search(self, root_state, root_node: Optional[MCTSNode] = None) -> Tuple[List[float], MCTSNode]:
        """
        Run MCTS simulations starting from root_state or an existing root_node.
        Returns action probabilities and the root node for reuse.
        """
        if root_node:
            root = root_node
            # Ensure the state is attached to the reused root
            root.state = root_state 
        else:
            root = MCTSNode(root_state)
        
        if not root.is_expanded:
            self._expand(root)
        
        for _ in range(self.num_simulations):
            node = root
            
            # 1. Selection
            while node.is_expanded and len(node.children) > 0:
                node = self._select_child(node)
            
            # 2. Expansion & Expansion Evaluation
            if not node.is_expanded:
                value = self._expand(node)
            else:
                # Terminal state value: If the game is already over, we use exact result
                value = 0.0
                if node.state and node.state.ended:
                    winner = node.state.winner
                    # Value is 1.0 if the player WHOSE TURN IT IS won
                    if winner is None: # Draw
                        value = 0.0
                    elif winner == node.state.current_player:
                        value = 1.0
                    else:
                        value = -1.0
            
            # 3. Backpropagation (Backup)
            self._backpropagate(node, value)
            
        # Return visit counts normalized
        counts = np.zeros(self.model.action_dim)
        for action_idx, child in root.children.items():
            if action_idx < len(counts):
                counts[action_idx] = child.visit_count
        
        # Normalize to probability distribution
        if counts.sum() > 0:
            return counts / counts.sum(), root
        else:
            # Fallback uniform
            return np.ones(self.model.action_dim) / self.model.action_dim, root

    def _select_child(self, node: MCTSNode) -> MCTSNode:
        """Select child using PUCT algorithm."""
        best_score = -float('inf')
        best_child = None
        
        # Using a single perspective: Values are stored relative to the layer's player
        for action_idx, child in node.children.items():
            u = self.c_puct * child.prior_prob * math.sqrt(node.visit_count) / (1 + child.visit_count)
            # Q is -child.value because child.value is from next player's perspective
            q_value = -child.value 
            
            score = q_value + u
            if score > best_score:
                best_score = score
                best_child = child
                
        return best_child or node

    def _expand(self, node: MCTSNode) -> float:
        """
        Expand leaf node using NN prediction.
        Returns: Value of the state (Leaf evaluation).
        """
        # Lazy simulation: only apply action when we actually need to expand or evaluate
        if node.state is None:
            if node.parent:
                node.state = self._apply_action(node.parent, node.action_idx)
            else:
                return 0.0 # Should not happen for root

        # Prepare for NN
        # Perspective must match the player WHOSE TURN IT IS in node.state
        p_idx = 0 if node.state.current_player == node.state.players[0] else 1
        self._temp_wrapper.perspective = p_idx + 1
        self._temp_wrapper._game = node.state
        state_data = self._temp_wrapper.get_state()
        
        # Encode state
        device = next(self.model.parameters()).device
        tensor = self.encoder.encode(state_data).unsqueeze(0).to(device)
        
        # Predict
        self.model.eval()
        with torch.no_grad():
            policy_probs, value = self.model(tensor)
            
        value = value.item()
        
        # Get valid actions from simulator (Expensive call, do it once per expansion)
        valid_actions = self._temp_wrapper.get_valid_actions()
        
        node.is_expanded = True
        
        # Create children using the valid actions found
        for act_obj in valid_actions:
             idx = act_obj.to_index()
             if idx not in node.children:
                 if idx < self.model.action_dim:
                     child = MCTSNode(state=None, parent=node, action_idx=idx, action_obj=act_obj)
                     child.prior_prob = policy_probs[0][idx].item()
                     node.children[idx] = child
        
        return value

    def _apply_action(self, parent_node: MCTSNode, action_idx: int):
        """
        Apply action_idx using the cached Action object if available.
        """
        # 1. Clone parent state
        new_game = parent_node.state.clone()
        
        # 2. Get the action object (Fast lookup)
        action_obj = None
        if action_idx in parent_node.children:
            action_obj = parent_node.children[action_idx].action_obj
        
        # 3. Use temp wrapper to step (No new instantiations)
        self._temp_wrapper._game = new_game
        
        if action_obj:
            # This step is now FAST because action_obj has _sim_action metadata
            self._temp_wrapper.step(action_obj)
        else:
            # Fallback (Slow path, shouldn't be hit often)
            fallback_act = Action.from_index(action_idx)
            self._temp_wrapper.step(fallback_act)
            
        return new_game

    def _backpropagate(self, node: MCTSNode, value: float):
        """Update node stats up to root."""
        current = node
        while current is not None:
            current.visit_count += 1
            current.value_sum += value
            current = current.parent
            value = -value # Perspective flip

