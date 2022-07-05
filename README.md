# Offer Helper Service
Helper service to get information from offer files not available in the Chia RPC.

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

`POST /get_offer_removals {"offer": "offer1..."}`