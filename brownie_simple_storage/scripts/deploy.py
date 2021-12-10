from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    account = get_account()
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


def get_account():
    if network.show_active() == 'development':
        return accounts[0]
    else:
        return accounts.add(config["wallets"]['from_key'])


def main():
    deploy_simple_storage()
