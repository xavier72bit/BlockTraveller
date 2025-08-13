# std import
import functools

# 3rd import
from flask import Flask, request, jsonify

# local import
from .node import Node
from ...core.block import Block
from ...core.transaction import Transaction


__all__ = ['HttpNode']


http = Flask('blockchain-http-node-single')

router_registry = {}
def http_route(rule, **options):
    """
    标记Node类的方法，将其与Flask.route绑定，并自动将返回值包装为json字符串
    """
    def decorator(method):
        router_registry[method.__name__] = (rule, options)
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            res = method(self, *args, **kwargs)
            return jsonify(res)
        return wrapper
    return decorator

# TODO: 解耦Node与API，自由组合

class HttpNode(Node):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def _register_router(self):
        """
        将当前类的方法，与flask app router绑定
        """
        for method_name, flask_router_args in router_registry.items():
            rule, options = flask_router_args
            http.route(rule, **options)(getattr(self, method_name))

    ################################################
    # Node
    ################################################

    @http_route('/alive', methods=['GET'])
    def _api_alive(self):
        return True

    @http_route('/join', methods=['POST'])
    def _api_join(self):
        pass

    ################################################
    # BlockChain
    ################################################

    @http_route('/blockchain', methods=['GET'])
    def _api_download_json(self):
        """
        下载json格式的区块链数据
        """
        return self.blockchain.to_json()

    @http_route('/block', methods=['POST'])
    def _api_add_block(self):
        block_data: dict = request.get_json()
        block = Block.deserialize(block_data)
        return self.blockchain.add_block(block)

    ################################################
    # Mining
    ################################################

    @http_route('/mining_data/<string:miner_addr>', methods=['GET'])
    def _api_apply_mining_data(self, miner_addr):
        """
        下载json格式的交易池数据
        """
        current_txpool = self.txpool.get_mining_data(miner_addr)
        return [t.serialize() for t in current_txpool]

    @http_route('/last_block', methods=['GET'])
    def _api_last_block(self):
        lb = self.blockchain.last_block
        return lb.serialize() if lb else None

    @http_route('/pow_check', methods=['GET'])
    def _api_pow_check(self):
        return self.blockchain.pow_check

    ################################################
    # user & transaction
    ################################################

    @http_route('/transaction', methods=['POST'])
    def _api_add_transaction(self):
        tx_data: dict = request.get_json()
        tx = Transaction.deserialize(tx_data)
        return self.txpool.add_transaction(tx)

    @http_route('/balance/<string:addr>')
    def _api_get_balance(self, addr):
        return self.blockchain.compute_balance(addr)

    @http_route('/prize/<string:addr>')
    def prize(self, addr):
        """
        空投奖励
        """
        return self.txpool.get_prize(addr, 100)

    def run(self):
        self._register_router()
        http.run(host=self.host, port=self.port)
