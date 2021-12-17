from scripts.helpful import get_account
from brownie import FundMe


def deploy_fund_me():
    account = get_account()
    fund_me = FundMe.deploy({"from": account})
    print(fund_me.address)


def main():
    deploy_fund_me()
