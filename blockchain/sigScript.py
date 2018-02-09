"""
Usage:
    sigScript.py sender recipient amount privateKeyB64

Options:
    --help    Show this help screen

"""
import sys
from Crypto.Hash import MD5
from wallet import Wallet

sender, recipient, amount, privateKeyB64 = [ argument.encode() for argument in sys.argv[1:] ]
transaction = sender + recipient + amount
hashedTransaction = MD5.new(transaction)

wallet = Wallet(privateKeyB64 = privateKeyB64)
signature = wallet.signature(hashedTransaction)


print ("      ┌─────────────────────────────────────────┐")
print ("      │      signature base64 output begins     │")
print ("──────┴─────────────────────────────────────────┴──────")
print (signature.decode())
print ("──────┬─────────────────────────────────────────┬──────")
print ("      │      signature base64 output ends       │")
print ("      └─────────────────────────────────────────┘")