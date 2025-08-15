# -*- coding: UTF-8 -*-
# @Project: core-impl-python
# @File   : http_peer_client.py
# @Author : Xavier Wu
# @Date   : 2025/8/13 20:35

# types hint
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...types.core_types import Transaction, Block
    from ...types.network_types import NetworkNodePeer

# 3rd import
import requests

# local import
from ..abstract.peer_client_adapter import PeerClientAdapter
from ..exceptions import PeerClientAdapterProtocolError


class HTTPPeerClientAdapter(PeerClientAdapter):
    def send_block(self, peer: NetworkNodePeer, block: Block):
        if peer.protocol != self.protocol():
            raise PeerClientAdapterProtocolError(f'peer: {peer.protocol}, adapter: {self.protocol()}')

    def send_tx(self, peer: NetworkNodePeer, tx: Transaction):
        if peer.protocol != self.protocol():
            raise PeerClientAdapterProtocolError(f'peer: {peer.protocol}, adapter: {self.protocol()}')

    def protocol(self) -> str:
        return 'http'
