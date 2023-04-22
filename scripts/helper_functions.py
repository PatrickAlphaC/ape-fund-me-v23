from ape import networks, accounts, project, config

# All local chains across "ecosystems" have the same name
LOCAL_CHAIN_NAMES = ["local", "development"]
FORKED_CHAIN_NAMES = ["mainnet-fork"]

CONTRACT_NAME_TO_MOCK = {
    "AggregatorV3Interface": project.MockV3Aggregator,
}


## Mock Contract Initial Values
DECIMALS = 8
INITIAL_VALUE = 2000_000000000000000000


def get_account(index=None, id=None, unlock_password=None):
    if index:
        return accounts[index]
    if id:
        account_to_use = accounts.load(id)
        if unlock_password:
            account_to_use.set_autosign(True, passphrase=unlock_password)
        return account_to_use
    if networks.active_provider.network.name in LOCAL_CHAIN_NAMES:
        return accounts.test_accounts[0]
    if (
        networks.active_provider.chain_id == 31337
        or networks.active_provider.chain_id == 1337
    ):
        account_to_use = accounts.load("local-default")
        if unlock_password:
            account_to_use.set_autosign(True, passphrase=unlock_password)
        return account_to_use
    # If none of the above...
    account_to_use = accounts.load("default")
    if unlock_password:
        account_to_use.set_autosign(True, passphrase=unlock_password)
    return account_to_use


def deploy_mocks():
    """
    Deploys mock contracts to a local network. Should take care to make sure you
    only call this function when running on a local network.
    """
    print(f"The active network is {networks.active_provider.network.name}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying mock v3 aggregator...")
    mock_price_feed = account.deploy(project.MockV3Aggregator, DECIMALS, INITIAL_VALUE)
    print(f"Deployed to {mock_price_feed.address}")
    print("Mocks Deployed!")


def get_or_deploy_contract(contract_name):
    """If you want to use this function, go to the ape config and add a new entry for
    the contract that you want to be able to 'get'. Then add an entry in the variable 'CONTRACT_NAME_TO_MOCK'.
    You'll see examples like the 'price_feed'.
        This script will then either:
            - Get a address from the config
            - Or deploy a mock to use for a network that doesn't have it

        Args:
            contract_name (name of ape.contracts.base.ContractContainer): This is the name that is referred to in the
            'CONTRACT_NAME_TO_MOCK' variable. It could be something like `project.AggregatorV3Interface`. It takes
            a contract or deployment on a real chain, and gets the mock version of it.

        Returns:
            contract
    """
    mock_contract_type = CONTRACT_NAME_TO_MOCK[contract_name]
    if (
        networks.active_provider.network.name in LOCAL_CHAIN_NAMES
        or networks.active_provider.chain_id == 31337
    ):
        if len(mock_contract_type.deployments) <= 0:
            deploy_mocks()
        contract = mock_contract_type.deployments[-1]
    else:
        try:
            ecosystem = networks.active_provider.network.ecosystem.name
            chain_name = networks.active_provider.network.name
            contract_addresses = [
                contract_and_address["address"]
                for contract_and_address in config.deployments[ecosystem][chain_name]
                if contract_and_address["contract_type"] == contract_name
            ]
            contract = mock_contract_type.at(contract_addresses[0])
        except KeyError:
            raise Exception(
                f"{networks.active_provider.network.name} address not found, perhaps you should add it to the ape-config.yaml or CONTRACT_NAME_TO_MOCK in the helper_functions.py file?"
            )
    return contract


def main():
    pass
