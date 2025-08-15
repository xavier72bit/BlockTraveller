class PeerClientProtocolError(Exception):
    """
    邻居Node的Protocol不支持
    """
    pass


class PeerClientAdapterProtocolError(Exception):
    """
    PeerClient所运行的网络协议与Adapter不匹配
    """
    pass