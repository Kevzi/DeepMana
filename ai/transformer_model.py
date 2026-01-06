"""Architecture de réseau moderne pour Hearthstone utilisant des Set Transformers.

Contrairement aux CNNs ou aux MLPs plates, cette architecture est invariante
par permutation, ce qui est idéal pour les ensembles de cartes (main, plateau).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from typing import Dict, List, Tuple, Optional


class MultiHeadAttention(nn.Module):
    """Multi-Head Self-Attention pour le Set Transformer."""
    
    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def forward(self, x, mask=None):
        batch_size = x.size(0)
        
        # Projection
        Q = self.W_q(x).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        
        # Scaled Dot-Product Attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        if mask is not None:
            # Mask must be [batch, 1, 1, seq_len] or [batch, 1, seq_len, seq_len]
            # Here we assume mask is [batch, seq_len] (True for padding)
            m = mask.unsqueeze(1).unsqueeze(2)
            scores = scores.masked_fill(m, float('-inf'))
            
            # Additional protection: if a whole row is -inf, softmax results in NaNs
            # This happens if a card cannot attend to anything (including itself)
            # which shouldn't happen for active cards, but can for padded cards.
            probs = F.softmax(scores, dim=-1)
            # Mask out NaNs for padded rows
            probs = probs.masked_fill(torch.isnan(probs), 0.0)
        else:
            probs = F.softmax(scores, dim=-1)
        
        out = torch.matmul(probs, V)
        
        # Concat heads
        out = out.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        return self.W_o(out)


class SetTransformerBlock(nn.Module):
    """Un bloc (SAB - Self-Attention Block) du Set Transformer."""
    
    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, n_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout)
        )
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Attention + Residual + LayerNorm
        attn_out = self.attention(x, mask)
        x = self.norm1(x + self.dropout(attn_out))
        
        # FFN + Residual + LayerNorm
        ffn_out = self.ffn(x)
        x = self.norm2(x + ffn_out)
        return x


class CardEncoder(nn.Module):
    """Encode une carte individuelle en combinant son ID et ses stats."""
    
    def __init__(self, card_vocab_size: int = 5000, d_model: int = 128):
        super().__init__()
        # Embedding pour l'identité de la carte
        self.card_embedding = nn.Embedding(card_vocab_size, d_model // 2)
        
        # Encoder pour les stats numériques
        self.stat_encoder = nn.Sequential(
            nn.Linear(10, d_model // 2),  # atk, hp, cost, etc.
            nn.GELU()
        )
        
        self.combine = nn.Linear(d_model, d_model)
    
    def forward(self, card_ids, card_stats):
        id_emb = self.card_embedding(card_ids)
        stat_emb = self.stat_encoder(card_stats)
        combined = torch.cat([id_emb, stat_emb], dim=-1)
        return self.combine(combined)


class HearthstoneTransformer(nn.Module):
    """Architecture State-of-the-Art pour Hearthstone."""
    
    def __init__(self, 
                 card_vocab_size: int = 5000,
                 d_model: int = 128,
                 n_heads: int = 4,
                 n_layers: int = 3,
                 action_dim: int = 300):
        super().__init__()
        
        self.d_model = d_model
        self.action_dim = action_dim
        
        self.card_encoder = CardEncoder(card_vocab_size, d_model)
        
        # Zones séparées pour plus de clarté structurelle
        self.hand_transformer = nn.ModuleList([
            SetTransformerBlock(d_model, n_heads, d_model * 4) for _ in range(n_layers)
        ])
        
        self.board_transformer = nn.ModuleList([
            SetTransformerBlock(d_model, n_heads, d_model * 4) for _ in range(n_layers)
        ])
        
        # Encoder pour l'état global (mana, hp, fatigue...)
        self.global_encoder = nn.Sequential(
            nn.Linear(20, d_model),
            nn.GELU(),
            nn.Linear(d_model, d_model)
        )
        
        # Pooling (Attention-based pooling pour ne pas perdre d'info)
        self.pool_attention = nn.Linear(d_model, 1)
        
        # Heads PPO (Actor-Critic)
        self.policy_head = nn.Sequential(
            nn.Linear(d_model * 4, d_model * 2),
            nn.GELU(),
            nn.Linear(d_model * 2, action_dim)
        )
        
        self.value_head = nn.Sequential(
            nn.Linear(d_model * 4, d_model),
            nn.GELU(),
            nn.Linear(d_model, 1)
        )
    
    def _pool(self, x, mask=None):
        """Attention-based pooling avec protection contre les NaNs (pour plateaux vides)."""
        # x shape: [batch, N, D]
        # mask shape: [batch, N] (True if masked/padding)
        
        weights = self.pool_attention(x)  # [batch, N, 1]
        
        if mask is not None:
            # Vérifier si toute la séquence est masquée pour chaque élément du batch
            # all_masked shape: [batch]
            all_masked = mask.all(dim=1)
            
            # Appliquer le masque
            weights = weights.masked_fill(mask.unsqueeze(-1), float('-inf'))
            
            # Softmax
            probs = F.softmax(weights, dim=1)
            
            # Si tout est masqué, forcer les probas à 0 pour éviter les NaNs
            # (On multiplie par ~all_masked pour mettre à 0 les lignes NaN)
            probs = probs.masked_fill(all_masked.unsqueeze(-1).unsqueeze(-1), 0.0)
            
            return (x * probs).sum(dim=1)
        
        weights = F.softmax(weights, dim=1)
        return (x * weights).sum(dim=1)
    
    def forward(self, hand_data, my_board_data, enemy_board_data, global_state, masks, action_mask=None):
        """Forward pass utilisant les différentes zones du jeu."""
        
        # 1. Encode cards
        # hand_data = (ids, stats)
        hand_emb = self.card_encoder(hand_data[0], hand_data[1])
        my_board_emb = self.card_encoder(my_board_data[0], my_board_data[1])
        enemy_board_emb = self.card_encoder(enemy_board_data[0], enemy_board_data[1])
        
        # 2. Transformers (Self-Attention inter-cartes)
        for block in self.hand_transformer:
            hand_emb = block(hand_emb, masks.get("hand"))
            
        for block in self.board_transformer:
            my_board_emb = block(my_board_emb, masks.get("my_board"))
            enemy_board_emb = block(enemy_board_emb, masks.get("enemy_board"))
            
        # 3. Pooling
        hand_p = self._pool(hand_emb, masks.get("hand"))
        my_p = self._pool(my_board_emb, masks.get("my_board"))
        en_p = self._pool(enemy_board_emb, masks.get("enemy_board"))
        global_emb = self.global_encoder(global_state)
        
        # 4. Concatenation & Heads
        combined = torch.cat([hand_p, my_p, en_p, global_emb], dim=-1)
        
        # Policy
        policy_logits = self.policy_head(combined)
        if action_mask is not None:
            policy_logits = policy_logits.masked_fill(action_mask == 0, float('-inf'))
        policy = F.softmax(policy_logits, dim=-1)
        
        # Value
        value = torch.tanh(self.value_head(combined))
        
        return policy, value
