from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
import base64
from Crypto.Hash import MD5


class Wallet:
    def __init__(self,privateKeyB64 = None):
        # If it's an instantiation with provided privateKeyB64, just import it.
        if privateKeyB64 is not None:
            privateKeyB64 = privateKeyB64.encode() if type(privateKeyB64) is str else privateKeyB64
            self.privateKey, self.privateKeyB64 = base64.b64decode(privateKeyB64), privateKeyB64
            
            # Instatiate _rsa by import private key
            self._rsa = RSA.importKey(self.privateKey)
        
        # If it's a new instance, generate one.
        else:
            randomGenerator = Random.new().read
            self._rsa = RSA.generate(2048, randomGenerator)

            # export private key
            self.privateKey = self._rsa.exportKey()
            self.privateKeyB64 = base64.b64encode(self.privateKey)

        # export public key
        self.publicKey = self._rsa.publickey().exportKey()
        self.publicKeyB64 = base64.b64encode(self.publicKey)

    @property
    def address(self):
        return self.publicKeyB64.decode()

    @property
    def secret(self):
        return self.privateKeyB64.decode()

    def signature(self, hashedTransaction):
        """
        Sign a hashed transaction

        :param hashedTransaction: hashed transaction for one wallet address.
        """

        signer = PKCS1_v1_5.new(self._rsa)
        signatureRaw = signer.sign(hashedTransaction)
        return base64.b64encode(signatureRaw)

    @staticmethod
    def verification(sender, recipient, amount, signature):
        """
        Verify a transaction for sender's wallet ownership check.

        :param sender:    <str> sender part of transaction to be verified
        :param recipient: <str> recipient part of transaction to be verified
        :param amount:    <str> amount part of transaction to be verified
        :param signature: <str> signature to be verified, it was encoded in base64 

        """

        transaction = "".join([str(part) for part in [sender, recipient, amount]]).encode()
        hashedTransaction = MD5.new(transaction)

        # Instantiate a rsa instance by importing the pub key AKA the sender address
        _rsa = RSA.importKey(base64.b64decode(sender.encode()))
        verifier = PKCS1_v1_5.new(_rsa)
        return verifier.verify(
            hashedTransaction, 
            base64.b64decode(signature.encode())
            )

