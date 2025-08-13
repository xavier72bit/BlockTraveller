# type hint
# types hint
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...types.network_types import API

# local import
from ...core.blockchain import BlockChain
from ...core.tx_pool import TransactionPool


class Node:
    def __init__(self, api: API):
        # 初始化Core组件
        self.blockchain = BlockChain(current_node=self)
        self.txpool = TransactionPool(current_node=self)

        # 设置API, 并建立绑定关系
        self.api = api
        self.api.set_node(self)

    def start(self):
        self.api.run()
