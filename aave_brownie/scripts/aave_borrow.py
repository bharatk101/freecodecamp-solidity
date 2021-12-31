from brownie import network, config, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from web3 import Web3

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config['networks'][network.show_active()]['weth_token']
    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    lending_pool = get_lending_pool()
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing!")
    tx = lending_pool.deposit(erc20_address, amount,
                              account.address, 0, {"from": account})
    tx.wait(1)
    print("Deposited!")
    # get borrowable data
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    # DAI to eth price
    dai_eth_price = get_assest_price(
        config['networks'][network.show_active()]['dai_eth_price_feed'])
    amount_dai_to_borrow = (1/dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow}")
    # borrow
    dai_address = config['networks'][network.show_active()]['dai_token']
    borrow_tx = lending_pool.borrow(dai_address, Web3.toWei(
        amount_dai_to_borrow, "ether"), 1, 0, account.address, {"from": account})
    borrow_tx.wait(1)
    print("we borrowed some DAI")
    get_borrowable_data(lending_pool, account)
    repay_all(amount, lending_pool, account)


def repay_all(amount, lending_pool, account):
    approve_erc20(Web3.toWei(amount, "ether"),
                  lending_pool,
                  config['networks'][network.show_active()]['dai_token'],
                  account
                  )

    repay_tx = lending_pool.repay(config['networks'][network.show_active(
    )]['dai_token'], amount, 1, account.address, {"from": account})
    repay_tx.wait(1)
    print("Repayed!")


def get_assest_price(price_feed_address):
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_price = Web3.fromWei(latest_price, "ether")
    print(f"Dai-Eth price is {converted_price}")
    return float(converted_price)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor) = lending_pool.getUserAccountData(account)

    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(available_borrow_eth, total_collateral_eth, total_debt_eth)
    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("Approvinf erc20 token")

    erc = interface.IERC20(erc20_address)
    tx = erc.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config['networks'][network.show_active(
        )]['lending_pool_addresses_provider']
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
