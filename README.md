# Offer Helper Service
Helper service to get information not available in the Chia RPC.

## Installing
Requires Python 3

Create a virtual environment, use that environment, and install the requirements

```
python3 -m venv venv
. ./venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Running
```
. ./venv/bin/activate
python3 ./main.py
```

Use the `PORT` environment variable or in the .env file to override the port

## Endpoints

### Get Offer Removals
Given an offer file get the coin id's which would be removed.

`POST /get_offer_removals`

```json
{
  "offer": "offer1..."
}
```
```json
[
    "0x975f8476b8343b79bda65880eecd499c90666c73bfd51f39d68720fe7ef2237f"
]
```

### Get NFT Minter's DID

`POST /get_minter_did_for_nft`

```json
{
    "coin_id":"nft1m9yldg9q922arzudt3cjgyzezagfk4exgaqne0gxhedj7mwq4kqqp4lzgs"
}
```

```json
{
    "did_coin_id": "0x28131414fed2de3b03cb4b6d851f06492aaa905d9e7aa28ec227c072d839696e",
    "did_id": "did:chia:19qf3g9876t0rkq7tfdkc28cxfy424yzanea29rkzylq89kped9hq3q7wd2"
}
```