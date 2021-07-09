from brownie import *
import brownie
import pytest


@pytest.mark.require_network("mainnet-fork")
def test_purchase(token, helper, sale):
    token.updateExempt(sale, True)
    token.transfer(sale, 100e18)
    helper.updateCharity(sale, [a[1]])
    sale.purchase(0, a[1], {'value': 10e18, 'from': a[1]})
    purchase = 10e18 / 5e15
    assert token.balanceOf.call(a[1])/1e18 == (purchase)/1e18


def test_try_purchase_zero(sale):
    with brownie.reverts():
        sale.purchase(0, a[1], {'from': a[1]})


def test_try_purchase_expired(token, helper, sale):
    token.updateExempt(sale, True)
    token.transfer(sale, 100e18)
    helper.updateCharity(sale, [a[1]])
    chain.sleep(86400 * 30 + 1)
    chain.mine()
    with brownie.reverts():
        sale.purchase(0, a[1], {'value': 1e18, 'from': a[1]})


def test_recover_tokens(token, helper, sale):
    token.transfer(sale, 5e18)
    chain.sleep(86400 * 240 + 1)
    chain.mine()
    old_balance = token.balanceOf.call(a[0])
    helper.updateAdmin(sale, a[0])
    sale.recover(token)
    assert token.balanceOf.call(a[0]) > old_balance

def test_recover_before_expired(token, helper, sale):
    with brownie.reverts():
        sale.recover(token)

def test_burn_tokens(token, helper, sale):
    token.transfer(sale, 5e18)
    chain.sleep(86400 * 30 + 1)
    chain.mine()
    sale.burn()

def test_burn_before_expired(sale):
    with brownie.reverts():
        sale.burn()

def test_purchase_below_min(token, helper, sale):
    token.transfer(sale, 100e18)
    helper.updateCharity(sale, [a[1]])
    with brownie.reverts():
        sale.purchase(100e18, a[1], {'value': 5e16, 'from': a[1]})

def test_purchase_donation_to_invalid_charity(token, helper, sale):
    token.updateExempt(sale, True)
    token.transfer(sale, 100e18)
    with brownie.reverts("Sale: Unknown charity"):
        sale.purchase(0, a[1], {'value': 10e18, 'from': a[1]})

def test_update_admin(sale, helper):
    helper.updateAdmin(sale, a[1])
    assert sale.admin.call() == a[1]

def test_not_admin(token, helper, sale):
    with brownie.reverts():
        helper.updateCharity(sale, [a[1]], {'from': a[1]})

    with brownie.reverts():
        sale.updateAdmin(a[1], {'from': a[1]})
    
    with brownie.reverts():
        helper.updateAdmin(sale, a[1], {'from': a[1]})

    chain.sleep(86400 * 240 + 1)
    chain.mine()
    with brownie.reverts():
        sale.recover(token, {'from': a[1]})


def test_estimate(sale):
    estimates = sale.estimate.call(1e18)
    clean = []
    for i in range(len(estimates)):
        clean.append(estimates[i]/1e18)
    print("User gets {} ASMR\nLiquidity gets {} ASMR and {} ETH\nCharity gets {} ETH\nFounder gets {} ETH".format(
        clean[0], clean[1], "0.5", clean[2], clean[3]
    ))
    sale.estimate(1e18)