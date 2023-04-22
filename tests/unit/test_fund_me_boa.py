import boa

from tests.conftest import SEND_VALUE


def test_price_feed_set_correctly(fund_me_boa):
    expected_version = 2
    price_feed_version = fund_me_boa.get_version()
    assert price_feed_version == expected_version


def test_fund_fails_without_enough_eth(fund_me_boa):
    with boa.reverts():
        fund_me_boa.fund()


def test_fund_updates_funded_data_structure(fund_me_boa):
    boa.env.set_balance(fund_me_boa.OWNER(), SEND_VALUE * 2)
    with boa.env.prank(fund_me_boa.OWNER()):
        fund_me_boa.fund(value=SEND_VALUE)
    amount_funded = fund_me_boa.address_to_amount_funded(fund_me_boa.OWNER())
    assert amount_funded == SEND_VALUE


def test_adds_funder_to_array_of_funders(fund_me_boa):
    boa.env.set_balance(fund_me_boa.OWNER(), SEND_VALUE * 2)
    with boa.env.prank(fund_me_boa.OWNER()):
        fund_me_boa.fund(value=SEND_VALUE)
    funder = fund_me_boa.funders(0)
    assert funder == fund_me_boa.OWNER()


def test_withdraw_from_single_funder(fund_me_boa_funded):
    starting_fund_me_balance = boa.env.get_balance(fund_me_boa_funded.address)
    starting_owner_balance = boa.env.get_balance(fund_me_boa_funded.OWNER())
    with boa.env.prank(fund_me_boa_funded.OWNER()):
        fund_me_boa_funded.withdraw()
    ending_fund_me_balance = boa.env.get_balance(fund_me_boa_funded.address)
    ending_owner_balance = boa.env.get_balance(fund_me_boa_funded.OWNER())
    assert ending_fund_me_balance == 0
    assert ending_owner_balance == starting_owner_balance + starting_fund_me_balance


def test_withdraw_from_multiple_funders(fund_me_boa_funded):
    number_of_funders = 10
    for i in range(number_of_funders):
        user = boa.env.generate_address(i)
        boa.env.set_balance(user, SEND_VALUE * 2)
        with boa.env.prank(user):
            fund_me_boa_funded.fund(value=SEND_VALUE)
    starting_fund_me_balance = boa.env.get_balance(fund_me_boa_funded.address)
    starting_owner_balance = boa.env.get_balance(fund_me_boa_funded.OWNER())

    with boa.env.prank(fund_me_boa_funded.OWNER()):
        fund_me_boa_funded.withdraw()

    assert boa.env.get_balance(fund_me_boa_funded.address) == 0
    assert starting_fund_me_balance + starting_owner_balance == boa.env.get_balance(
        fund_me_boa_funded.OWNER()
    )
