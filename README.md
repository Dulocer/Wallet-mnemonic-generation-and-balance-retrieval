# Finding a needle in a haystack
Searching for habitable planets in the universe.
Generate wallet mnemonics (12 words) and retrieve the BTC and USDT balances in the wallet.

A simple Python program will generate two files after running: "wallet with balance.csv" and "mnemonic.csv".

"Mnemonic.csv" will record the wallets that have been generated to ensure that the program will not generate duplicate mnemonics the next time it runs;
"Wallet with balance.csv" will record the wallets with balance.

# The number of wallets that can be generated in one run

```python
# Number of wallets to generate
num_wallets = 50000  # Here you can set the number of wallets to be generated
