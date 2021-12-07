from brownie import accounts, config, SimpleStorage


def deploy_simple_storage():
    account = accounts[0]
    print(account)
    # account = accounts.load("freecodecamp-account")
    # print(account)
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)

    # deploy contract
    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)

    # load value
    stored_value = simple_storage.retrive()
    print(stored_value)

    # update value
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)

    # get the updated value
    updated_stored_value = simple_storage.retrive()
    print(updated_stored_value)


def main():
    deploy_simple_storage()
