from typing import Optional

from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_record import CoinRecord
from chia.util.bech32m import decode_puzzle_hash, encode_puzzle_hash
from chia.util.config import load_config_cli
from chia.wallet.did_wallet.did_info import DID_HRP
from chia.wallet.nft_wallet.nft_info import NFT_HRP
from chia.wallet.nft_wallet.uncurry_nft import UncurriedNFT
from flask import Flask, request, jsonify
from chia.wallet.trading.offer import Offer
from chia.full_node.full_node import FullNode
from chia.util.default_root import DEFAULT_ROOT_PATH
from dotenv import load_dotenv
from os import getenv
import asyncio

from FakeServer import FakeServer
from GetPuzzleProgram import get_puzzle_program

load_dotenv()
api = Flask(__name__)

SERVICE_NAME = "full_node"
config = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", SERVICE_NAME)
overrides = config["network_overrides"]["constants"][config["selected_network"]]
updated_constants = DEFAULT_CONSTANTS.replace_str_to_bytes(**overrides)
fullNodeService = FullNode(config, root_path=DEFAULT_ROOT_PATH, consensus_constants=updated_constants)
fullNodeService.set_server(FakeServer())
loop = asyncio.get_event_loop()
coroutine = fullNodeService._start()
loop.run_until_complete(coroutine)


@api.route("/get_offer_removals", methods=["POST"])
def get_offer_removals():
    offer_hex: str = request.json["offer"]
    offer = Offer.from_bech32(offer_hex)
    coins = offer.removals()
    offered_coin_ids = [f"0x{coin.name()}" for coin in coins]
    return jsonify(offered_coin_ids)


@api.route("/get_minter_did_for_nft", methods=["POST"])
async def get_minter_did_for_nft():
    coin_id = request.json["coin_id"]
    if coin_id.startswith(NFT_HRP):
        coin_id = decode_puzzle_hash(coin_id)
    else:
        coin_id = bytes32.from_hexstr(coin_id)

    coin_record: Optional[CoinRecord] = await fullNodeService.blockchain.coin_store.get_coin_record(coin_id)
    if coin_record is None:
        raise ValueError(f"Nft coin record 0x{coin_id.hex()} not found")

    launched_coin = await fullNodeService.blockchain.coin_store.get_coin_records_by_parent_ids(include_spent_coins=True,
                                                                                               parent_ids=[coin_id])
    first_nft_spend = await fullNodeService.blockchain.coin_store.get_coin_records_by_parent_ids(
        include_spent_coins=True,
        parent_ids=[launched_coin[0].coin.name()])
    first_nft_spend_puzzle = await get_puzzle_program(first_nft_spend[0], fullNodeService)
    uncurried_nft: UncurriedNFT = UncurriedNFT.uncurry(first_nft_spend_puzzle)
    response = {"did_coin_id": "0x" + uncurried_nft.owner_did.hex(), "did_id": encode_puzzle_hash(uncurried_nft.owner_did, DID_HRP)}
    return jsonify(response)

if __name__ == "__main__":
    api.run(port=getenv("PORT") or 5000)
