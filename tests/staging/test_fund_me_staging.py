import ape
import pytest
from scripts.helper_functions import get_account

SEND_VALUE = 1_000_000_000_000_000_000  # 1 ether


@pytest.mark.staging
def test_can_fund_and_withdraw(fund_me_contract_ape, account):
    fund_me_contract_ape.fund(sender=account, value=SEND_VALUE)
    amount_funded = fund_me_contract_ape.address_to_amount_funded(account.address)
    assert amount_funded == SEND_VALUE

    fund_me_contract_ape.withdraw(sender=account)
    assert fund_me_contract_ape.balance == 0
