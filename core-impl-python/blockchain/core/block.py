# types hint
from __future__ import annotations

# local import
from .transaction import Transaction
from ..exceptions import DeserializeHashValueCheckError
from ..tools.hash_tools import compute_hash


class Block:
    """
    区块
    """
    __slots__ = [
        'index', 'timestamp', 'transactions', 'nonce', 'prev_hash', 'hash',
        '_runtime_is_from_peer'
    ]
    frozen_fields = (
        'index', 'timestamp', 'transactions', 'nonce', 'prev_hash', 'hash',
        '_runtime_is_from_peer'
    )
    # 序列化、反序列化时的字段
    serialized_fields = ('index', 'timestamp', 'transactions', 'nonce', 'prev_hash', 'hash')

    def __init__(self, index, timestamp, transactions: list[Transaction], nonce, prev_hash):
        ## core data
        object.__setattr__(self, 'index', index)
        object.__setattr__(self, 'timestamp', timestamp)
        object.__setattr__(self, 'transactions', transactions)
        object.__setattr__(self, 'nonce', nonce)
        object.__setattr__(self, 'prev_hash', prev_hash)

        ## hash
        object.__setattr__(self, 'hash', self.compute_hash())

        self.__init_system_fields()

    def __init_system_fields(self):
        ## block系统运行时标记
        object.__setattr__(self, '_runtime_is_from_peer', False)
        
    @property
    def is_from_peer(self):
        return self._runtime_is_from_peer

    def mark_from_peer(self):
        object.__setattr__(self, '_runtime_is_from_peer', True)

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

        for f in cls.serialized_fields:
            if f == 'transactions':  # 单独单独处理TX的反序列化
                object.__setattr__(
                    b, f,
                    [Transaction.deserialize(d) for d in data.get(f, [])]
                )
                continue

            if f == 'hash':  # 跳过hash字段的赋值
                continue

            object.__setattr__(b, f, data.get(f, None))

        # hash一致性检查
        computed_hash = b.compute_hash()
        data_hash = data.get('hash', None)
        if computed_hash == data_hash:
            object.__setattr__(b, 'hash', computed_hash)
        else:
            raise DeserializeHashValueCheckError(f"Block Data compute hash: {computed_hash}, data hash: {data_hash}")

        b.__init_system_fields()
        return b

    def serialize(self) -> dict:
        d = {}
        for f in self.serialized_fields:
            if f == 'transactions':  # 单独单独处理TX的序列化
                d[f] = [t.serialize() for t in getattr(self, f)]
                continue
            d[f] = getattr(self, f)

        return d

    def set_from_peer(self):
        """
        将区块标记为从其他node广播得来
        """
        object.__setattr__(self, '_runtime_is_from_peer', True)
