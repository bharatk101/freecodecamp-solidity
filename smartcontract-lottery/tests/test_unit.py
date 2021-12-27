from _pytest.config import exceptions
from brownie import accounts, Lottery, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery, enter_lottery
from web3 import Web3
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENV, get_account, fund_with_link, get_contract
import pytest


def test_get_entereance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    # arrange
    lottery = deploy_lottery()
    # act
    expected_enterance_fee = Web3.toWei(0.025, "ether")
    enterance_fee = lottery.getEnteranceFee()
    # assert
    assert expected_enterance_fee == enterance_fee


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    # arrange
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter(
            {"from": get_account(), "value": lottery.getEnteranceFee()})


def test_can_start_and_enter():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    # arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    player_account = get_account()
    lottery.enter({"from": player_account, "value": lottery.getEnteranceFee()})
    assert lottery.players(0) == player_account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    # arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    player_account = get_account()
    lottery.enter({"from": player_account, "value": lottery.getEnteranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    # arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": get_account(index=1),
                  "value": lottery.getEnteranceFee()})
    lottery.enter({"from": get_account(index=2),
                  "value": lottery.getEnteranceFee()})
    lottery.enter({"from": get_account(index=3),
                  "value": lottery.getEnteranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({"from": account})
    requestId = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RND = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, STATIC_RND, lottery.address, {"from": account})
    #  777 % 3 = 0 the winner is the first player
    winner = get_account(index=1)
    starting_balance_winner = winner.balance()
    balance_of_lottery = lottery.balance()
    assert lottery.recentWinner() == winner
    assert lottery.balance() == 0
    assert winner.balance() == starting_balance_winner + balance_of_lottery
