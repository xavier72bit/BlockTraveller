# std import
import json
import hashlib

from ..exceptions import DeserializeHashValueCheckError
# local import
from ..tools.hash_tools import compute_hash
from ..tools.ecdsa_sign_tools import ECDSATool


class Transaction:
    """
    Transaction - 交易信息对象
    """
    __slots__ = [
        'saddr', 'raddr', 'amount', 'timestamp', 'hash', 'signature',
        '_runtime_is_confirmed', '_runtime_is_from_peer'
    ]
    frozen_fields = (
        'saddr', 'raddr', 'amount', 'timestamp', 'hash',
        '_runtime_is_confirmed', '_runtime_is_from_peer'
    )
    # 序列化、反序列化时的字段
    serialized_fields = ('saddr', 'raddr', 'amount', 'timestamp', 'hash', 'signature',)

    def __init__(self, saddr: str | None, raddr: str, amount: int, timestamp: int):
        ## core data
        object.__setattr__(self, 'saddr', saddr)  # sender public key, None is miner reward
        object.__setattr__(self, 'raddr', raddr)  # recipient public key
        object.__setattr__(self, 'amount', amount)  # 目前仅支持int类型的交易数量
        object.__setattr__(self, 'timestamp', timestamp)  # 交易时间

        ## hash & signature
        object.__setattr__(self, 'hash', self.compute_hash())
        self.signature = None

        self.__init_system_fields()

    def __init_system_fields(self):
        ## tx pool交互
        object.__setattr__(self, '_runtime_is_confirmed', False)
        object.__setattr__(self, '_runtime_is_from_peer', False)

    @property
    def is_confirmed(self) -> bool:
        return self._runtime_is_confirmed

    def mark_confirmed(self):
        """
        将交易标记为已确认
        """
        # TODO: 检测调用者, 打log
        object.__setattr__(self, '_runtime_is_confirmed', True)

    def mark_unconfirmed(self):
        """
        将交易标记为未确认
        """
        # TODO: 检测调用者, 打log
        object.__setattr__(self, '_runtime_is_confirmed', False)

    @property
    def is_from_peer(self):
        return self._runtime_is_from_peer

    def mark_from_peer(self):
        # TODO: 检测调用者, 打log
        object.__setattr__(self, '_runtime_is_from_peer', True)

    def __setattr__(self, key, value):
        if key in self.frozen_fields:
            raise AttributeError(f'key {key} is frozen')

        super().__setattr__(key, value)

    def __delattr__(self, item):
        if item in self.frozen_fields:
            raise AttributeError(f'key {item} is frozen')

        super().__delattr__(item)

    def tx_core_data(self) -> dict:
        """
        交易核心数据，参与hash计算

        :return:
        """
        return {
            'saddr': self.saddr,
            'raddr': self.raddr,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def compute_hash(self) -> str:
        tx_json = json.dumps(self.tx_core_data(), sort_keys=True).encode()
        return hashlib.sha256(tx_json).hexdigest()

    def sign(self, sec_key: str):
        """
        对交易数据进行签名, 流程为:
            交易的核心数据hash -> 私钥签名 -> 保存到signature字段

        :param sec_key: str
        :return:
        """
        ecdsa_tool = ECDSATool(secret_key=sec_key)

        object.__setattr__(self, 'signature', ecdsa_tool.sign_data(self.hash.encode()))

    def verify_sign(self) -> bool:
        """
        验证交易是否有效
        :return:
        """
        # 系统交易
        if self.saddr is None:
            return True

        if self.signature is None:
            return False

        ecdsa_tool = ECDSATool(public_key=self.saddr)
        return ecdsa_tool.verify_sign_data(self.signature, self.hash.encode())

    @classmethod
    def deserialize(cls, data: dict | None) -> "Transaction | None":
        """
        从dict加载数据，同时进行验证

        :param data:
        :return:
        """
        if data is None:
            return None

        t = object.__new__(cls)
        for f in cls.serialized_fields:
            if f == 'hash':  # 跳过hash字段的赋值
                continue
            object.__setattr__(t, f, data.get(f, None))

        # hash一致性检查
        computed_hash = t.compute_hash()
        data_hash = data.get('hash', None)
        if computed_hash == data_hash:
            print('pass')
            object.__setattr__(t, 'hash', computed_hash)
        else:
            raise DeserializeHashValueCheckError(f"TX Data compute hash: {computed_hash}, data hash: {data_hash}")

        t.__init_system_fields()
        return t

    def serialize(self) -> dict:
        d = {}
        for f in self.serialized_fields:
            d[f] = getattr(self, f)

        return d
