from Crypto.PublicKey import RSA
import Crypto.Random
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import binascii

class Wallet:

    def __init__(self):
        self.private_key = None
        self.public_key = None




    def create_keys(self):
        private_key,public_key  = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key




    def save_keys(self):
        if self.private_key != None and self.public_key != None :
            try:
                with open('wallet.txt','w') as f :
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
            except (IOError,IndexError):
                print("Saving Wallet Error !")

    def load_key(self):
        try:
            with open('wallet.txt','r') as f :
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]

                self.public_key = public_key
                self.private_key = private_key
        except(IOError,IndexError):
            print("loading wallet error!")

    def generate_keys(self):
        private_key = RSA.generate(1024,Crypto.Random.new().read)
        #bind the private key with the public key
        public_key = private_key.publickey()
        #'DER' binary encoding
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
                binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))


    def sign_transaction(self,sender, recipient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        print(signer)
        h= SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        print(h)
        signature = signer.sign(h)

        return binascii.hexlify(signature).decode('ascii')