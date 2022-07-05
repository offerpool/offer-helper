from flask import Flask, json, request
from chia.wallet.trading.offer import Offer
from dotenv import load_dotenv
from os import getenv

load_dotenv()
api = Flask(__name__)


@api.route("/get_offer_removals", methods=["POST"])
def get_offer_removals():
    offer_hex: str = request.json["offer"]
    offer = Offer.from_bech32(offer_hex)
    coins = offer.removals()
    offered_coin_ids = [f"0x{coin.name()}" for coin in coins]
    return json.dumps(offered_coin_ids)


if __name__ == "__main__":
    api.run(port=getenv("PORT") or 5000)
