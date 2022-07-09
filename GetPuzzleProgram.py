# Ripped from Chia RPC with minor changes
from typing import Optional
from chia.full_node.full_node import FullNode
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_record import CoinRecord
from chia.types.full_block import FullBlock
from chia.types.generator_types import BlockGenerator
from chia.full_node.mempool_check_conditions import get_puzzle_and_solution_for_coin


async def get_puzzle_program(coin_record: CoinRecord, full_node_service: FullNode) -> Optional[Program]:
    coin_name: bytes32 = coin_record.coin.name()
    height = coin_record.spent_block_index
    header_hash = full_node_service.blockchain.height_to_hash(height)
    assert header_hash is not None
    block: Optional[FullBlock] = await full_node_service.block_store.get_full_block(header_hash)

    if block is None or block.transactions_generator is None:
        raise ValueError("Invalid block or block generator")

    block_generator: Optional[BlockGenerator] = await full_node_service.blockchain.get_block_generator(block)
    assert block_generator is not None
    error, puzzle, solution = get_puzzle_and_solution_for_coin(
        block_generator, coin_name, full_node_service.constants.MAX_BLOCK_COST_CLVM
    )
    if error is not None:
        raise ValueError(f"Error: {error}")

    return Program.to(puzzle)
