import pytest
import ape
import boa
import os
from dotenv import load_dotenv
from scripts.deploy_fund_me import deploy_fund_me, get_account
from scripts.helper_functions import DECIMALS, INITIAL_VALUE

load_dotenv()


SEND_VALUE = 1_000_000_000_000_000_000  # 1 ether


@pytest.fixture(scope="module")
def wallet_password():
    return os.getenv("WALLET_PASSWORD")


# DANGER! Only use this for CI/CD!!
# Remember to NEVER push your password or encrypted key!!
@pytest.fixture(scope="module")
def account(wallet_password):
    return get_account(unlock_password=wallet_password)


@pytest.fixture
def fund_me_contract_ape(wallet_password) -> ape.contracts.base.ContractInstance:
    return deploy_fund_me(unlock_password=wallet_password)


@pytest.fixture
def fund_me_boa(project) -> boa.vyper.contract.VyperContract:
    aggregator = boa.load(project.MockV3Aggregator.source_path, DECIMALS, INITIAL_VALUE)
    return boa.load(project.FundMe.source_path, aggregator.address)


@pytest.fixture
def fund_me_boa_funded(fund_me_boa) -> boa.vyper.contract.VyperContract:
    boa.env.set_balance(fund_me_boa.OWNER(), SEND_VALUE * 2)
    with boa.env.prank(fund_me_boa.OWNER()):
        fund_me_boa.fund(value=SEND_VALUE)
    return fund_me_boa
