from brownie import SimpleStorage
from scripts.helpful_scripts import get_account


def deploy():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    tx = simple_storage.store(1, {"from": account})
    tx.wait(1)
    print(tx.events)


def main():
    deploy()
