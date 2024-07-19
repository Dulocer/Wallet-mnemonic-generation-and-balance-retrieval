import os
import hashlib
import binascii
import csv
import requests
from mnemonic import Mnemonic
import bip32utils
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import threading

CSV_FILE = 'Mnemonic.csv'
BALANCE_CSV_FILE = 'Wallet with balance.csv'

# 创建锁对象
lock = threading.Lock()

def load_existing_mnemonics(csv_file):
    if not os.path.exists(csv_file):
        return set()
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return {row[0] for row in reader if row}

def save_mnemonic_to_csv(csv_file, mnemonic):
    with open(csv_file, mode='a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([mnemonic])

def generate_entropy(bits=128):
    return os.urandom(bits // 8)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def get_checksum_bits(entropy_hex):
    entropy_bytes = binascii.unhexlify(entropy_hex)
    hash_hex = sha256(entropy_bytes)
    hash_bits = bin(int(hash_hex, 16))[2:].zfill(256)
    checksum_length = len(entropy_hex) * 4 // 32
    return hash_bits[:checksum_length]

def entropy_with_checksum(entropy_hex):
    entropy_bits = bin(int(entropy_hex, 16))[2:].zfill(len(entropy_hex) * 4)
    checksum_bits = get_checksum_bits(entropy_hex)
    return entropy_bits + checksum_bits

def bits_to_mnemonic(bits):
    mnemo = Mnemonic("english")
    bits_chunks = [bits[i:i + 11] for i in range(0, len(bits), 11)]
    indices = [int(chunk, 2) for chunk in bits_chunks]
    words = [mnemo.wordlist[index] for index in indices]
    return ' '.join(words)

def generate_mnemonic(bits=128):
    entropy = generate_entropy(bits)
    entropy_hex = entropy.hex()
    bits_with_checksum = entropy_with_checksum(entropy_hex)
    return bits_to_mnemonic(bits_with_checksum)

def mnemonic_to_seed(mnemonic, passphrase=""):
    mnemo = Mnemonic("english")
    return mnemo.to_seed(mnemonic, passphrase)

def seed_to_private_key(seed):
    root_key = bip32utils.BIP32Key.fromEntropy(seed)
    return root_key

def get_address_balance_blockchain_info(address):
    try:
        url = f"https://blockchain.info/q/addressbalance/{address}"
        response = requests.get(url)
        if response.status_code == 200:
            balance = int(response.text) / 1e8  # Convert from Satoshi to BTC
            return balance
        else:
            return None
    except Exception as e:
        return None

def get_address_balance_blockcypher(address):
    try:
        url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
        response = requests.get(url)
        if response.status_code == 200:
            balance = response.json()['final_balance'] / 1e8  # Convert from Satoshi to BTC
            return balance
        else:
            return None
    except Exception as e:
        return None

def get_address_balance(address):
    balance = get_address_balance_blockchain_info(address)
    if balance is None:
        balance = get_address_balance_blockcypher(address)
    return balance

def get_usdt_balance(address):
    try:
        url = "https://api.omniexplorer.info/v1/address/addr/overview/"
        params = {'addr': address}
        response = requests.post(url, data=params)
        if response.status_code == 200:
            data = response.json()
            for balance in data['balance']:
                if balance['symbol'] == 'USDT':
                    return float(balance['value'])
        return 0.0
    except Exception as e:
        return None

def process_wallet(existing_mnemonics):
    while True:
        mnemonic_phrase = generate_mnemonic(128)
        with lock:
            if mnemonic_phrase not in existing_mnemonics:
                existing_mnemonics.add(mnemonic_phrase)
                save_mnemonic_to_csv(CSV_FILE, mnemonic_phrase)
                break
    
    seed = mnemonic_to_seed(mnemonic_phrase)
    root_key = seed_to_private_key(seed)
    address = root_key.Address()
    btc_balance = get_address_balance(address)
    usdt_balance = get_usdt_balance(address)
    
    with lock:
        if btc_balance is not None and btc_balance > 0:
            save_mnemonic_to_csv(BALANCE_CSV_FILE, mnemonic_phrase)
        elif usdt_balance is not None and usdt_balance > 0:
            save_mnemonic_to_csv(BALANCE_CSV_FILE, mnemonic_phrase)
    
    return mnemonic_phrase, btc_balance, usdt_balance

# Number of wallets to generate(The actual number of records is twice the set value)
num_wallets = 5000  # Here you can set the number of wallets to be generated

existing_mnemonics = load_existing_mnemonics(CSV_FILE)

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_wallet, existing_mnemonics) for _ in range(num_wallets)]

    with tqdm(total=num_wallets) as pbar:
        for future in as_completed(futures):
            future.result()
            pbar.update(1)
