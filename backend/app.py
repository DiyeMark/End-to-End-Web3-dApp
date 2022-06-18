import json
import os

from flask import Flask, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import datetime
from dotenv import load_dotenv

# from algosdk.v2client import algod
# from algosdk import account, mnemonic
# from algosdk.future.transaction import AssetConfigTxn
# from algosdk.future.transaction import *
# from backend.helpers.AssetHelper import print_created_asset, print_asset_holding
from backend.databases.db import initialize_db
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (JWTManager,
                                jwt_required)

from backend.resources.error import errors
from backend.resources.routes import initialize_routes

app = Flask(__name__)
# app.config.from_envvar('ENV_FILE_LOCATION')


api = Api(app, errors=errors)
bcrypt = Bcrypt(app)

# JWT Config
# app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_SECRET_KEY"] = "JwT-S3cR3t-K3y-F0:V3nTG3m3nAy3B0t"
jwt = JWTManager(app)


# Mongo Config
mongo_db_host = os.getenv('MONGO_HOST')
app.config["MONGODB_SETTINGS"] = {
    # 'host': f'mongodb://{mongo_db_host}:27017/10Academy_Certificate_Db'
    'host': 'mongodb://localhost:27017/10Academy_Certificate_Db'
}
initialize_db(app)

initialize_routes(api)

'''
def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

    # My address:
    # VGASUU2OGPGTUEBTF4YSBJHLGT6IGDAXYHVMFTOLDJRRKWOAPAFG2OZZKI
    # My private key:
    # YpEBFcXql0UfGKS+qXzzVWB59vJsCgXCIkdghDaHOb6pgSpTTjPNOhAzLzEgpOs0/IMMF8Hqws3LGmMVWcB4Cg==
    # My passphrase:
    # clump alien melody proof cool sphere science piano daughter verify whale aim version rural guide apology doll mention castle ecology home gift vault absent inject

    # My address:
    # SSMU6EM7QLXDQEEWPNRFG7LJTLZTFZCAUM5HDTIA6SPDTKJ7OZXPDVMA64
    # My private key:
    # 3tQfXMmLFB6Zf1DOosxxb21PiUY3UISrqbxGbMpncfSUmU8Rn4LuOBCWe2JTfWma8zLkQKM6cc0A9J45qT92bg==
    # My passphrase:
    # orange leg puppy route cinnamon elegant wolf expire flush crater rib street paddle pelican riot expand identify pluck furnace settle network fly phone abstract detect

    # My address:
    # PHPBEK2VR4EGQDUXVLMD4VRBGOQWP4HD65SOKZNU2K46YTAUGUU4NGZSR4
    # My private key:
    # fDc0pGU3AsmRmcIUdyJjxKFFspih95zKgIE/Kd7kWL153hIrVY8IaA6Xqtg+ViEzoWfw4/dk5WW00rnsTBQ1KQ==
    # My passphrase:
    # usage speak spirit iron afford inch smart secret tip mean cover brisk mercy clutch art waste fatal add school negative rough decrease turn absent horn


# Shown for demonstration purposes. NEVER reveal secret mnemonics in practice.
# Change these values with your mnemonics
mnemonic1 = "clump alien melody proof cool sphere science piano daughter verify whale aim version rural guide apology doll mention castle ecology home gift vault absent inject"
mnemonic2 = "orange leg puppy route cinnamon elegant wolf expire flush crater rib street paddle pelican riot expand identify pluck furnace settle network fly phone abstract detect"
mnemonic3 = "usage speak spirit iron afford inch smart secret tip mean cover brisk mercy clutch art waste fatal add school negative rough decrease turn absent horn"
# never use mnemonics in production code, replace for demo purposes only

# For ease of reference, add account public and private keys to
# an accounts dict.
accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

# Specify your node address and token. This must be updated.
# algod_address = ""  # ADD ADDRESS
# algod_token = ""  # ADD TOKEN

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

# CREATE ASSET
# Get network params for transactions before every transaction.
params = algod_client.suggested_params()


def create_asset(public_key, for_student):
    txn = AssetConfigTxn(
        sender=accounts[1]['pk'],
        sp=params,
        total=1,
        default_frozen=False,
        asset_name="10 Academy Certificate - " + for_student,
        manager=accounts[2]['pk'],
        reserve=accounts[2]['pk'],
        freeze=accounts[2]['pk'],
        clawback=accounts[2]['pk'],
        url="",
        decimals=0
    )
    # Sign with secret key of creator
    stxn = txn.sign(accounts[1]['sk'])
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)
    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))
    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, accounts[1]['pk'], asset_id)
        print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
    except Exception as e:
        print(e)


def modify_asset():
    pass


def receive_asset():
    pass


def freeze_asset():
    pass


def destroy_asset():
    pass


def transfer_asset():
    pass
'''


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/health")
def health():
    """health route"""
    state = {"status": "UP"}
    return jsonify(state)


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
