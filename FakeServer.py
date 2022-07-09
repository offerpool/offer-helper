from typing import List, Callable

from chia.server.outbound_message import Message, NodeType
from chia.types.blockchain_format.sized_bytes import bytes32


class FakeServer:
    async def send_to_all(self, messages: List[Message], node_type: NodeType):
        pass

    async def send_to_all_except(self, messages: List[Message], node_type: NodeType, exclude: bytes32):
        pass

    def set_received_message_callback(self, callback: Callable):
        pass