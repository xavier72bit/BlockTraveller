# types hint
from __future__ import annotations

# local import
from .transaction import Transaction
from ..tools.hash_tools import compute_hash


class Block:
    """
    区块
    """
    __slots__ = ['index', 'timestamp', 'transactions', 'nonce', 'prev_hash', 'hash']
    frozen_fields = ('index', 'timestamp', 'transactions', 'nonce', 'prev_hash', 'hash')
    core_fields = ('index', 'timestamp', 'transactions', 'nonce', 'prev_hash', 'hash')

    def __init__(self, index, timestamp, transactions: list[Transaction], nonce, prev_hash):
        ## core data
        object.__setattr__(self, 'index', index)
        object.__setattr__(self, 'timestamp', timestamp)
        object.__setattr__(self, 'transactions', transactions)
        object.__setattr__(self, 'nonce', nonce)
        object.__setattr__(self, 'prev_hash', prev_hash)

        ## hash
        object.__setattr__(self, 'hash', self.compute_hash())

    def __setattr__(self, name, value):
        if name in self.frozen_fields:
            raise AttributeError(f'key {name} is frozen')

        super().__setattr__(name, value)

    def __delattr__(self, name):
        if name in self.frozen_fields:
            raise AttributeError(f'key {name} is frozen')

        super().__delattr__(name)

    def block_core_data(self) -> dict:
        """
        区块核心数据，参与hash计算

        :return:
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [t.serialize() for t in self.transactions],
            'nonce': self.nonce,
            'prev_hash': self.prev_hash
        }

    def compute_hash(self) -> str:
        """
        区块的哈希算法

        :return: str
        """
        return compute_hash(self.block_core_data())

    @classmethod
    def deserialize(cls, data: dict | None) -> "Block | None":
        """
        从dict加载数据
        """
        if data is None:
            return None

        b = object.__new__(cls)

        for f in cls.__slots__:
            if f == 'transactions':
                object.__setattr__(
                    b, f,
                    [Transaction.deserialize(d) for d in data.get(f, [])]
                )
                continue
            object.__setattr__(b, f, data.get(f, None))

        return b

    def serialize(self) -> dict:
        d = {}
        for f in self.__slots__:
            if f == 'transactions':
                d[f] = [t.serialize() for t in getattr(self, f)]
                continue
            d[f] = getattr(self, f)

        return d
