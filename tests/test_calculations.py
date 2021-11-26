import pytest
from app.calculations import *
import time

@pytest.fixture()
def zero_bank_account():
    return BankAccount()

@pytest.fixture()
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,5),
    (7,1,8),
    (12,3,15)
])
def test_add(num1, num2, expected):
    assert add(num1,num2) == expected
def test_sub():
    assert sub(1,2) == -1

def test_mul():
    assert mul(1,2) == 2

def test_div():
    assert div(4,2) == 2


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_bank_test_withraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,5) == 55

@pytest.mark.parametrize("deposited, withdrew, expected",[
    (3000,2000,1000),
    (500,450,50),
    (10,3,7)
])
def test_bank_transaction(zero_bank_account:BankAccount, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account:BankAccount):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(500)