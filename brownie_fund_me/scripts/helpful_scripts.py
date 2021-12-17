from brownie import config, network, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
decimals = 18
starting_price = 200000000000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(decimals, starting_price, {"from": get_account()})
