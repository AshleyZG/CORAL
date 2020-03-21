import torch.nn as nn

from .transformer import TransformerBlock
from .embedding import BERTEmbedding
from .utils import PositionwiseFeedForward, LayerNorm
import pdb


class BERT(nn.Module):
    """
    BERT model : Bidirectional Encoder Representations from Transformers.
    """

    def __init__(self, vocab_size, hidden=768, n_layers=12, attn_heads=12, dropout=0.1):
        """
        :param vocab_size: vocab_size of total words
        :param hidden: BERT model hidden size
        :param n_layers: numbers of Transformer blocks(layers)
        :param attn_heads: number of attention heads
        :param dropout: dropout rate
        """

        super().__init__()
        self.hidden = hidden
        self.n_layers = n_layers
        self.attn_heads = attn_heads

        # paper noted they used 4*hidden_size for ff_network_hidden_size
        self.feed_forward_hidden = hidden * 4

        # embedding for BERT, sum of positional, segment, token embeddings
        self.embedding = BERTEmbedding(
            vocab_size=vocab_size, embed_size=hidden, dropout=dropout)

        # multi-layers transformer blocks, deep network
        self.transformer_blocks = nn.ModuleList(
            [TransformerBlock(hidden, attn_heads, hidden * 4, dropout) for _ in range(n_layers)])
        self.feedforward = PositionwiseFeedForward(
            d_model=hidden, d_ff=hidden * 4, dropout=dropout)
        self.layernorm = LayerNorm(hidden)

    def forward(self, x, segment_info, adj_mat, train):
        # pdb.set_trace()
        # attention masking for padded token
        # torch.ByteTensor([batch_size, 1, seq_len, seq_len)
        # mask = (x > 0).unsqueeze(1).repeat(1, x.size(1), 1).unsqueeze(1)
        mask = adj_mat
        # embedding the indexed sequence to sequence of vectors
        # if not train:
        #     pdb.set_trace()
        x = self.embedding(x, segment_info, train)
        # x = self.layernorm(x)
        # running over multiple transformer blocks
        for transformer in self.transformer_blocks:
            x = transformer.forward(x, mask, train)
            x = self.layernorm(x + self.feedforward(x))
        return x
