# types hint
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...types.node_types import Node

# std import
from abc import abstractmethod, ABC


__all__ = ['API']


class API(ABC):
    def __init__(self):
        self.node = None
        self.blockchain = None
        self.txpool = None

    def set_node(self, node: Node):
        self.node = node
        self.blockchain = self.node.blockchain
        self.txpool = self.node.txpool

    ################################################
    # Node API
    ################################################

    @abstractmethod
    def _api_alive(self):
        """
        心跳检测
        """
        pass

    @abstractmethod
    def _api_join(self):
        """
        请求节点加入网络
        """

    ################################################
    # BlockChain API
    ################################################

    @abstractmethod
    def _api_download(self):
        """
        下载区块链数据
        """
        pass

    @abstractmethod
    def _api_add_block(self):
        """
        添加区块
        """

    @abstractmethod
    def _api_last_block(self):
        """
        获取最后一个区块的数据
        """
        pass

    ################################################
    # Mining API
    ################################################

    @abstractmethod
    def _api_apply_mining_data(self):
        """
        申请挖矿的区块数据
        """
        pass

    @abstractmethod
    def _api_pow_check(self):
        """
        检查Proof of Work
        """
        pass

    ################################################
    # user & transaction API
    ################################################

    @abstractmethod
    def _api_add_transaction(self):
        """
        新增交易数据
        """
        pass

    @abstractmethod
    def _api_get_balance(self, addr):
        """
        获取指定地址的余额
        """
        pass

    @abstractmethod
    def _api_prize(self, addr):
        """
        给指定地址空投奖励
        """
        pass


    ################################################
    # object function
    ################################################

    @abstractmethod
    def run(self):
        """
        启动API服务
        """
        pass
