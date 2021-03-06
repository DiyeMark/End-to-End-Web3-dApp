import json

from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn
from algosdk.future.transaction import *
from backend.helpers.AssetHelper import print_created_asset, print_asset_holding

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


class Asset:
    def __init__(self):
        pass

    def create_asset(self, for_student):
        # CREATE ASSET
        # Get network params for transactions before every transaction.
        params = algod_client.suggested_params()
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

    def modify_asset(self):
        pass

    def receive_asset(self, asset_id):
        # OPT-IN
        # Check if asset_id is in account 3's asset holdings prior
        # to opt-in
        params = algod_client.suggested_params()
        # comment these two lines if you want to use suggested params
        # params.fee = 1000
        # params.flat_fee = True
        account_info = algod_client.account_info(accounts[3]['pk'])
        holding = None
        idx = 0
        for my_account_info in account_info['assets']:
            scrutinized_asset = account_info['assets'][idx]
            idx = idx + 1
            if scrutinized_asset['asset-id'] == asset_id:
                holding = True
                break
        if not holding:
            # Use the AssetTransferTxn class to transfer assets and opt-in
            txn = AssetTransferTxn(
                sender=accounts[3]['pk'],
                sp=params,
                receiver=accounts[3]["pk"],
                amt=0,
                index=asset_id)
            stxn = txn.sign(accounts[3]['sk'])
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
            # Now check the asset holding for that account.
            # This should now show a holding with a balance of 0.
            print_asset_holding(algod_client, accounts[3]['pk'], asset_id)

    def transfer_asset(self, asset_id):
        # TRANSFER ASSET
        # transfer asset of 10 from account 1 to account 3
        params = algod_client.suggested_params()
        # comment these two lines if you want to use suggested params
        # params.fee = 1000
        # params.flat_fee = True
        txn = AssetTransferTxn(
            sender=accounts[1]['pk'],
            sp=params,
            receiver=accounts[3]["pk"],
            amt=1,
            index=asset_id)
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
        # The balance should now be 10.
        print_asset_holding(algod_client, accounts[3]['pk'], asset_id)

    def freeze_asset(self):
        pass

    def destroy_asset(self):
        pass


# asset = Asset()
# asset.create_asset(for_student="Denamo")
# Asset ID: 95970040
# asset.receive_asset(asset_id=95970040)
# asset.transfer_asset(asset_id=95970040)