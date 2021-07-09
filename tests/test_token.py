from brownie import *
import brownie

FEE = 3e17

def test_token_transfer(token):
    token.transfer(a[1], 100e18)
    token.transfer(a[1], 100e18, {'from': a[1]})
    assert token.balanceOf.call(a[1]) == 100e18 - FEE

def test_token_transfer_exempt(token):
    # Transfer FROM exempt
    token.transfer(a[1], 100e18)
    assert token.balanceOf.call(a[1]) == 100e18
    # Transfer TO exempt
    balance = token.balanceOf.call(a[0])
    token.transfer(a[0], 100e18, {'from': a[1]})
    assert token.balanceOf.call(a[0]) == balance + 100e18

def test_token_transfer_from(token):
    token.approve(a[1], 100e18)
    token.transferFrom(a[0], a[1], 100e18, {'from': a[1]})
    assert token.balanceOf.call(a[1]) == 100e18

def test_not_admin(token):
    with brownie.reverts():
        token.updateExempt(a[1], True, {'from': a[1]})
    
    with brownie.reverts():
        token.updateAdmin(a[1], {'from': a[1]})

def test_change_admin(token):
    token.updateAdmin(a[1])
    assert token.admin.call() == a[1]