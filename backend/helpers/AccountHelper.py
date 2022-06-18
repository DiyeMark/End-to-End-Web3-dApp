from algosdk import account, mnemonic


def generate_algorand_keypair():
    private_key, address = account.generate_account()

    return address, private_key, mnemonic.from_private_key(private_key)