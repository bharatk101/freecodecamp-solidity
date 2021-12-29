from brownie import BoToken
from web3 import Web3
from scripts.helpful_scripts import get_account


initial_supply = Web3.toWei(1000, "ether")


def deploy_contract():
    account = get_account()
    bo_token = BoToken.deploy(initial_supply, {"from": account})
    print(bo_token.name())


def main():
    deploy_contract()
