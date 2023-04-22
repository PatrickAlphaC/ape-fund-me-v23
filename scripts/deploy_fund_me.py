from ape import project, networks
from scripts.helper_functions import get_account, get_or_deploy_contract
from scripts.helper_config import network_config


def deploy_fund_me(unlock_password=None) -> project.FundMe:
    account = get_account(unlock_password=unlock_password)
    price_feed = get_or_deploy_contract("AggregatorV3Interface")

    ecosystem = networks.active_provider.network.ecosystem.name
    chain_name = networks.active_provider.network.name
    publish = (
        network_config.get(ecosystem, {}).get(chain_name, {}).get("publish", False)
    )

    fund_me = account.deploy(
        project.FundMe,
        price_feed.address,
        publish=publish,
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
