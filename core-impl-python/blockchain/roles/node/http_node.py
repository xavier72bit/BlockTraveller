# std import
import functools

# 3rd import
from flask import Flask, request, jsonify

# local import
from .node import Node
from ...core.block import Block
from ...core.transaction import Transaction


__all__ = ['NodeHttpSingle']


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


class NodeHttpSingle(Node):
    def _register_router(self):
        """
        将当前类的方法，与flask app router绑定
        """
        for method_name, flask_router_args in router_registry.items():
            rule, options = flask_router_args
            http.route(rule, **options)(getattr(self, method_name))

    @http_route('/alive', methods=['GET'])
    def alive(self):
        return True

    @http_route('/', methods=['GET'])
    def download_json(self):
        """
        下载json格式的区块链数据
        """
        return self.blockchain.to_json()

    @http_route('/mining_data/<string:miner_addr>', methods=['GET'])
    def apply_mining_data(self, miner_addr):
        """
        下载json格式的交易池数据
        """
        current_txpool = self.txpool.get_mining_data(miner_addr)
        return [t.serialize() for t in current_txpool]

    @http_route('/transaction', methods=['POST'])
    def add_transaction(self):
        tx_data: dict = request.get_json()
        tx = Transaction.deserialize(tx_data)
        return self.txpool.add_transaction(tx)

    @http_route('/last_block', methods=['GET'])
    def last_block(self):
        lb = self.blockchain.last_block
        return lb.serialize() if lb else None

    @http_route('/pow_check', methods=['GET'])
    def pow_check(self):
        return self.blockchain.pow_check

    @http_route('/block', methods=['POST'])
    def add_block(self):
        block_data: dict = request.get_json()
        block = Block.deserialize(block_data)
        return self.blockchain.add_block(block)

    @http_route('/balance/<string:addr>')
    def get_balance(self, addr):
        return self.blockchain.compute_balance(addr)

    @http_route('/prize/<string:addr>')
    def prize(self, addr):
        return self.txpool.get_prize(addr, 100)

    def run(self):
        self._register_router()
        http.run(port=5000)
