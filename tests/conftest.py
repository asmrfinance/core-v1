from brownie import *
import pytest 

UNISWAP = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D" # Uniswap V2 Router address

@pytest.fixture
def token(AltruisticToken):
    yield a[0].deploy(AltruisticToken)

@pytest.fixture
def helper(SaleHelper):
    yield a[0].deploy(SaleHelper)

@pytest.fixture
def sale(token, helper, AltruisticSale):
    yield a[0].deploy(AltruisticSale, UNISWAP, token, helper, chain.time() + 86400 * 30)

@pytest.fixture
def timelock(TimelockController):
    yield a[0].deploy(TimelockController, 50, [a[0]], [a[0]])