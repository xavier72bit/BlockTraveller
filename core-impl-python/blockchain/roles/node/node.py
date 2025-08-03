from ...core.blockchain import BlockChain
from ...core.tx_pool import TransactionPool


class Node:
    def __init__(self):
        self.blockchain = BlockChain(current_node=self)
        self.txpool = TransactionPool(current_node=self)
