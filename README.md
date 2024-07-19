# Finding a needle in a haystack
Searching for habitable planets in the universe.
Generate wallet mnemonics (12 words) and retrieve the BTC and USDT balances in the wallet.

A simple Python program will generate two files after running: "wallet with balance.csv" and "mnemonic.csv".

"Mnemonic.csv" will record the wallets that have been generated to ensure that the program will not generate duplicate mnemonics the next time it runs;
"Wallet with balance.csv" will record the wallets with balance.

# The number of wallets that can be generated in one run

```python
# Number of wallets to generate(The actual number of records is twice the set value)
num_wallets = 5000  # Here you can set the number of wallets to be generated
'''

# Pip install
pip install mnemonic bip32utils tqdm

# Thank you for your use
If this app really helps you, could you give me some tokens to buy chips?

<span style="display:none">
XMR
467uP2E4Q6KPAHgxcD9qjpDDJyuqLds6vS7SSwmGdxYLdqFqpzQiEdVEx3fUd7kfCCJKDTTSa8GShUbZyHARwWYcJNsnLGz

USDT（Arbitrum）
0xA9baaDe9dB4B6AA2237BD46bd40bd7849De5D66b

USDC（Arbitrum）
0xA9baaDe9dB4B6AA2237BD46bd40bd7849De5D66b
</span>
