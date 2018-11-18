from functools import reduce
import json
from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification



MINING_REWARD = 10

blockchain = []
open_transcations = []
owner = "hatem"


def get_balance(participant):
    """ calculate and return a balance of a participant

        :participant: the person od whom to calculate the balance
    """
    tx_sender = [[tx.amount for tx in block.transactions
                  if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transcations if tx.sender == participant]
    tx_sender.append(open_tx_sender)

    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx.amount for tx in block.transactions
                     if tx.recipient == participant] for block in blockchain]

    amount_recived = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,
                            tx_recipient, 0)

    return amount_recived - amount_sent


def get_last_blockchain__value():
    """Returns the last value of the current blockchain"""
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def load_data():
    global blockchain
    global open_transcations

    try:
        with open('blockchain.txt', 'r') as f:
            file_content = f.readlines()

            blockchain = json.loads(file_content[0][:-1])

            # get all the returns blocks data ordered like we save them
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in
                                block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'],
                                      block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain

            # transactions updated
            open_transcations = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transcations:
                updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transcations = updated_transactions

    except (IOError, ValueError, IndexError):
        print("file not found so we initialize the blockchain with the genesis block")
        genesis_block = Block(0, '', [], 0, 0)
        blockchain = [genesis_block]
        open_transcations = []
    finally:
        print('CleanUp!!')


load_data()


def save_data():
    try:
        with open('blockchain.txt', 'w') as f:
            savebal_blockchain = [block.__dict__ for block in [
                Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions],
                      block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(savebal_blockchain))
            f.write('\n')
            savebal_tx = [tx.__dict__ for tx in open_transcations]
            f.write(json.dumps(savebal_tx))
    except IOError:
        print('Saving Error!!')


def add_transaction(recipient, amount, sender=owner):
    """ Append a new value as well as the last blockchain value  to the blockchain

     Arguments:
         :sender : the sender of the coins.
         :recipient: the recipient of the coins.
         :amount: the amount of coins sent with the transcations (default =1.0)

    """

    transaction = Transaction(sender, recipient, amount)

    ver = Verification()
    if ver.verify_transaction(transaction, get_balance):
        open_transcations.append(transaction)
        save_data()
        return True

    return False


# calculation the Nonce numbre
def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    ver = Verification()
    while not ver.valid_proof(open_transcations, last_hash, proof):
        proof += 1

    return proof


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    proof = proof_of_work()

    reward_transaction = Transaction('MINING', owner, MINING_REWARD)

    # for reason of invalid transaction so there is no reward so must make a copy the open_transactions
    # if we cant mine a block
    copied_transactions = open_transcations[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)

    return True


def get_transaction_value():
    """returns the input of the user (a new transaction amount) as a float"""

    tx_recipient = input("enter the recipeint of the transation : ")
    tx_amount = float(input('you tranction amount please: '))
    return tx_recipient, tx_amount


def get_user_choice():
    return input("Your choice : ")


def print_blockchain_elements():
    # output the blockchain list to the console
    for block in blockchain:
        print("outputting blocks:")
        print(block)
    else:
        print("-" * 20)


while True:
    print("Please choose")
    print("1.Add a new transaction value ")
    print("2.Mine a new block")
    print("3.Output the blockchain blocks ")
    print("4.check transactions validity")
    print("q.Quit")
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount):
            print("added transaction !")
        else:
            print("transaction failed!")

        print(open_transcations)
    elif user_choice == '2':
        if mine_block():
            open_transcations = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        ver = Verification()
        if ver.verify_transactions(open_transcations, get_balance):
            print("all transactions are valid")
        else:
            print("there are invalid transactions")

    elif user_choice == 'q':
        break
    else:
        print("Wrong input value, Please pick a value from te list")

    ver = Verification()
    if not ver.verify_chain(blockchain):
        print_blockchain_elements()
        print("invalid blockchain!")
        break
    print('Balance of {} is : {:6.2f} BTC'.format("hatem", get_balance('hatem')))
print('Done!')
