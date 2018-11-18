from hash_util import hash_block, hash_string_256


class Verification:

    def valid_proof(self, transaction, last_block, proof):
        """ validating a hash of the block with a specification

            :transaction: transactions stored in the block
            :last_block: last_block hash
            :proof : proof of work number (NONCE)

        """
        guess = (str([tx.to_ordered_dict() for tx in transaction]) + str(last_block) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        print(guess_hash)

        return guess_hash[0:2] == '00'


    def verify_chain(self, blockchain):
        """ verify the current blockchain and return true if the blockchain is valid

            :blockchain: verify the entire blockchain

        """

        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue

            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid !!")
                return False

        return True


    def verify_transaction(self,transaction, get_balance):
        """  verify a transaction wether the sender has sifficiant coins

            :transaction: the transaction that shoud be verfied
        """
        sender_balance = get_balance(transaction.sender)

        return sender_balance >= transaction.amount


    def verify_transactions(self, open_transcations, get_balance):
        """ verify all transactions """
        return all([self.verify_transaction(tx, get_balance) for tx in open_transcations])
