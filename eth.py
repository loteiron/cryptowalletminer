import asyncio
from web3 import Web3
import secrets
from colorama import Fore, Style
import random
from concurrent.futures import ThreadPoolExecutor

# Birden fazla Alchemy API endpoint'ini tanımla
infura_urls = [
    "https://eth-mainnet.g.alchemy.com/v2/L4ZghkCyOLkHdDZeT5yIy80zuD_sUA4n",
    "https://eth-mainnet.g.alchemy.com/v2/4Qnu24uw1gKhaFwNvwANK4NuVvAhzmY5",
    "https://eth-mainnet.g.alchemy.com/v2/aSv-wBARK7jzYdJPS45cnbb8FpEEJHv7",
    "https://eth-mainnet.g.alchemy.com/v2/kteRcnfbx8oUtkZ172Slu1geDq2lbTqI",
    "https://eth-mainnet.g.alchemy.com/v2/UNnsZcuKx6HS0f8Gjs6DHCuUnqrQMNOg",
    "https://eth-mainnet.g.alchemy.com/v2/44VQ77h7-ICIxTlBlrMflOR5ubj6yE0U",
    "https://eth-mainnet.g.alchemy.com/v2/fnfGxhi-VP8O1X9Ji199BAm8Dq5KWRdd"
    "https://eth-mainnet.g.alchemy.com/v2/ppQPodzvA0E5Lmv5QDEg5VWHXNVXq-n6"
    # İstediğin kadar endpoint ekleyebilirsin
]

def generate_private_key():
    # Özel anahtar oluştur
    private_key_bytes = secrets.token_bytes(32)
    private_key_hex = private_key_bytes.hex()
    return private_key_hex

def get_ethereum_balance(private_key):
    # Rastgele bir Alchemy API URL'si seç
    infura_url = random.choice(infura_urls)
    
    # Web3 sağlayıcısını başlat
    web3 = Web3(Web3.HTTPProvider(infura_url))
    
    # Özel anahtardan Ethereum adresini türet
    account = web3.eth.account.from_key(private_key)
    address = account.address

    # Ethereum adresinin bakiyesini al
    balance = web3.eth.get_balance(address)

    # Wei'yi Ether'e dönüştür
    balance_in_ether = web3.from_wei(balance, 'ether')
    return address, balance_in_ether

def save_private_key_to_file(private_key):
    # Bakiyesi sıfır olmayan Ethereum adreslerini kaydet
    with open("private_keys.txt", "a") as file:
        file.write(private_key + "\n")

async def process_address(executor):
    private_key = await asyncio.get_event_loop().run_in_executor(executor, generate_private_key)
    address, balance = await asyncio.get_event_loop().run_in_executor(executor, get_ethereum_balance, private_key)
    
    print(Fore.RED + "Address:", address, Fore.GREEN + "Balance:", balance, Fore.RED + "Private Key:", private_key)
    
    if balance > 0:
        await asyncio.get_event_loop().run_in_executor(executor, save_private_key_to_file, private_key)

async def main():
    # ThreadPoolExecutor ile 200 threads kullan
    executor = ThreadPoolExecutor(max_workers=150)
    
    count = 0
    while True:
        # 200 adet paralel görev başlat
        tasks = [process_address(executor) for _ in range(150)]
        await asyncio.gather(*tasks)
        count += 150
        print(Fore.YELLOW + "Count:", count)

asyncio.run(main())
