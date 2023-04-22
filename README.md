<!-- How to create a new project with all the boilerplate:

1. ape init
2. copy paste the `pyproject.toml`
3. copy paste the `pytest.ini`
4. copy paste the .gitignore
5. copy paste the .env
6. run `poetry install` -->


# Getting Started

It's recommended that you've gone through the [apeworx getting started documentation](https://docs.apeworx.io/ape/stable/userguides/quickstart.html) before proceeding here. 


## Requirements

- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - You'll know you did it right if you can run `git --version` and you see a response like `git version x.x.x`
- [Python](https://www.python.org/downloads/)
  - You'll know you've installed python right if you can run:
    - `python --version` or `python3 --version` and get an ouput like: `Python x.x.x`
- [pip](https://pypi.org/project/pip/)
  - You'll know you did it right if you can run `pip --version` or `pip3 --version` and get an output like `pip x.x from /some/path/here (python x.x)`
- [poetry](https://python-poetry.org/docs/)
  - You'll know you did it right if you can run `poetry --version` and get an output like `Poetry version (x.x.x)`

## Quickstart 

1. Clone the repo

```bash
git clone https://github.com/patrickalphac/ape-fund-me-v23
cd ape-fund-me-v23
```

2. Install dependencies

```bash
poetry install 
poetry run ape plugins install alchemy vyper ape-etherscan
```

3. Run unit tests

```
poetry run pytest
```

# Usage

## Testnet - Sepolia 

1. Import an account

To import an account into ape, run the following:

```bash
poetry run ape accounts import default
```

Where `default` will be the name of your account. Ape will then prompt you for your private key and password, and encrypt it on your computer. The only way to use this key moving forward will be to decrypt the key with your password. 

See [this faucet](https://faucets.chain.link/) for testnet tokens. 

2.  Set your RPC_URL

Since we are working with Alchemy, create an [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) called `WEB3_ALCHEMY_PROJECT_ID` or `WEB3_ALCHEMY_API_KEY`. If using a linux or mac environment, you can set it by running:

```
export WEB3_ALCHEMY_PROJECT_ID=MY_API_TOKEN
```

3. Run your script!

```
poetry run ape run scripts/deploy_fund_me.py --network ethereum:sepolia:alchemy
```


## Staging Tests

🛑 **WARNING** 🛑
*Run staging tests sparingly!* 
*We didn't write them for this project*

1. Add your wallet password as an environment variable

```
export WALLET_PASSWORD=xxxx
```
(or place into your `.env`)


To run staging tests, after running the above run:

```
poetry run ape test -m "staging" --network ethereum:sepolia:alchemy
```

This will test your contracts on a testnet.

# Formatting

```
poetry run black ./contracts/*.vy
```

# Storage layout 

```
poetry run vyper -f layout contracts/example_contracts/FunWithStorage.vy > fun_with_storage_layout.json
```

# Verification

Verification is currently pretty wonky for vyper. Right now to verify a contract:

1. Manually flatten the contract
2. Deploy the contract
   1. This means, you'll have to convert all your interface imports to in-line imports
3. Verify on the etherscan UI
4. You'll need to be familiar with constructor abi-encoding

```
cast abi-encode "__init__(address)" 0x694AA1769357215DE4FAC081bf1f309aDC325306
```

Then remove the `0x` prefix.