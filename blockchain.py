from functools import reduce
import json
from utility.hash_util import hash_block
from block import Block
from transaction import Transaction
from utility.verification import Verification

MINING_REWARD = 10


class Blockchain:

    def __init__(self,hosting_node_id):
        self.genesis_block = Block(0, '', [], 0, 0)
        self.chain = [self.genesis_block]
        self.__open_transcations = []
        self.load_data()
        self.hosting_node = hosting_node_id



    @property
    def chain(self):
        """ getter proprety (gettion just a  copy"""
        return self.__chain[:]


    @chain.setter
    def chain(self,val):
        self.__chain = val



    def get_open_transactions(self):
        """ just return a copy"""
        return self.__open_transcations[:]

    def get_last_blockchain__value(self):
        """Returns the last value of the current blockchain"""
        if len(self.__chain) < 1:
            return None

        return self.__chain[-1]


    def load_data(self):


        try:
            with open('blockchain.txt', 'r') as f:
                file_content = f.readlines()

                blockchain = json.loads(file_content[0][:-1])

                # get all the returns blocks data ordered like we save them
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'],tx['signature'], tx['amount']) for tx in
                                    block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'],
                                          block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain

                # transactions updated
                open_transcations = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transcations:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'],tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transcations = updated_transactions

        except (IOError, ValueError, IndexError):
            print("file not found so we initialize the blockchain with the genesis block")
        finally:
            print('CleanUp!!')



    def get_balance(self):
        """ calculate and return a balance of a participant

        """

        participant = self.hosting_node

        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transcations if tx.sender == participant]
        tx_sender.append(open_tx_sender)

        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]

        amount_recived = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,
                                tx_recipient, 0)

        return amount_recived - amount_sent

    def save_data(self):
        try:
            with open('blockchain.txt', 'w') as f:
                savebal_blockchain = [block.__dict__ for block in [
                    Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions],
                          block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(savebal_blockchain))
                f.write('\n')
                savebal_tx = [tx.__dict__ for tx in self.__open_transcations]
                f.write(json.dumps(savebal_tx))
        except IOError:
            print('Saving Error!!')


    def add_transaction(self, recipient, sender, signature, amount ):
        """ Append a new value as well as the last blockchain value  to the blockchain

         Arguments:
             :sender : the sender of the coins.
             :recipient: the recipient of the coins.
             :amount: the amount of coins sent with the transcations (default =1.0)

        """
        if self.hosting_node == None:
            return False

        transaction = Transaction(recipient,sender,signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance()):
            self.__open_transcations.append(transaction)
            self.save_data()
            return True

        return False


    # calculation the Nonce numbre
    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transcations, last_hash, proof):
            proof += 1

        return proof


    def mine_block(self):

        if self.hosting_node == None:
            return False

        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING' ,self.hosting_node, '', MINING_REWARD)
        # for reason of invalid transaction so there is no reward so must make a copy the open_transactions
        # if we cant mine a block
        copied_transactions = self.__open_transcations[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        self.__chain.append(block)
        self.open_transcations = []
        self.save_data()

        return True


