import torch
import torch.nn as nn
import torch.nn.functional as F

class HearthstoneModel(nn.Module):
    """
    Neural Network for Hearthstone AI.
    
    Architecture:
    - Input: Game State Tensor
    - Hidden Layers: Fully Connected (MLP)
    - Heads:
        - Policy Head: Probabilities for each action (Action Space Size)
        - Value Head: Scalar evaluation of current state (-1 to 1)
    """
    
    def __init__(self, input_dim, action_dim):
        super(HearthstoneModel, self).__init__()
        
        self.input_dim = input_dim
        self.action_dim = action_dim
        self.hidden_dim = 512  # Increased for Hearthstone complexity
        
        # Shared Layers (3 layers for better representation)
        self.fc1 = nn.Linear(input_dim, self.hidden_dim)
        self.fc2 = nn.Linear(self.hidden_dim, self.hidden_dim)
        self.fc3 = nn.Linear(self.hidden_dim, 256)  # Bottleneck before heads
        self.dropout = nn.Dropout(0.1)
        
        # Policy Head (Actor)
        self.policy_head = nn.Linear(256, action_dim)
        
        # Value Head (Critic)
        self.value_head = nn.Linear(256, 1)
        
    def forward(self, x, action_mask=None):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = F.relu(self.fc3(x))
        
        # Policy: Logits -> Mask -> Softmax
        policy_logits = self.policy_head(x)
        
        if action_mask is not None:
            # Set invalid actions to -inf so they receive 0 probability after softmax
            policy_logits = policy_logits.masked_fill(action_mask == 0, float('-inf'))
            
        policy = F.softmax(policy_logits, dim=-1)
        
        # Value: Tanh (-1 to 1)
        value = torch.tanh(self.value_head(x))
        
        return policy, value
