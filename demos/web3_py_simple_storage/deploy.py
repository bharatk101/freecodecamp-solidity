from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# save json bytecode
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect to blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

# Create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get nonce
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

# create transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId":chain_id, "gasPrice": w3.eth.gas_price, "from":my_address, "nonce":nonce})

#  sign transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

#send tracsaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash)

# working with transaction
simple_storage = w3.eth.contract(address=tx_reciept.contractAddress, abi=abi)

#  two ways to interact call and transact
# Call -> simulate a call and getting a return value, no change in state
# Transact -> Make a state change

#  get fav number
print(simple_storage.functions.retrive().call())

# make transaction
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId":chain_id, "gasPrice": w3.eth.gas_price, "from":my_address, "nonce":nonce+1}
)
signed_store_tx = w3.eth.account.sign_transaction(store_transaction, private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_storage.functions.retrive().call())