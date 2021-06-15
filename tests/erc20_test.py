import pytest

from brownie import accounts, reverts, ERC20

NAME = "Tacocoin"
SYMBOL = "TCC"
DECIMALS = 18
TOTAL_SUPPLY = 10 ** DECIMALS

@pytest.fixture(scope="module")
def erc20():
    return accounts[0].deploy(ERC20, NAME, SYMBOL, DECIMALS, TOTAL_SUPPLY)

def test_balance(erc20):
    assert erc20.balanceOf(accounts[0]) == TOTAL_SUPPLY
    assert erc20.balanceOf(accounts[1]) == 0

def test_transfer(erc20):
    erc20.transfer(accounts[1], 1000)
    assert erc20.balanceOf(accounts[0]) == (TOTAL_SUPPLY - 1000)
    assert erc20.balanceOf(accounts[1]) == 1000
    
    with reverts("Amount exceeds owner's balance"):
        erc20.transfer(accounts[0], 2000, {'from': accounts[1]})

def test_allowances_approvals(erc20):
    assert erc20.allowance(accounts[1], accounts[0]) == 0
    erc20.approve(accounts[0], 500, {'from': accounts[1]})
    assert erc20.allowance(accounts[1], accounts[0]) == 500
    
def test_transferFrom(erc20):
    with reverts("Amount exceeds allowance for spender"):
        erc20.transferFrom(accounts[1], accounts[0], 1000)
    
    assert erc20.balanceOf(accounts[1]) == 1000
    assert erc20.allowance(accounts[1], accounts[0]) == 500
    erc20.transferFrom(accounts[1], accounts[0], 500)
    assert erc20.allowance(accounts[1], accounts[0]) == 0
    assert erc20.balanceOf(accounts[1]) == 500
    
    erc20.approve(accounts[0], 2**256-1, {'from': accounts[1]})
    with reverts("Amount exceeds owner's balance"):
        erc20.transferFrom(accounts[1], accounts[0], 501)