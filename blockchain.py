from functools import reduce
import json
from collections import OrderedDict
from hash_util import hash_block,hash_string_256

MINING_REWARD = 10

blockchain = []
open_transcations = []
owner = "hatem"
participants = {'hatem'}



def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transaction'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transcations if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)

    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block['transaction'] if tx['recipient'] == participant] for block in
                    blockchain]
    amount_recived = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,
                            tx_recipient, 0)

    return amount_recived - amount_sent


def get_last_blockchain__value():
    """Returns the last value of the current blockchain"""
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])

    return sender_balance >= transaction['amount']


def load_data():
    global blockchain
    global open_transcations

    try:
        with open('blockchain.txt','r') as f :
            file_content = f.readlines()


            blockchain = json.loads(file_content[0][:-1])

            #get all the returns blocks data ordered like we save them
            updated_blockchain = []
            for block in blockchain:
                updated_block = {
                                'previous_hash': block['previous_hash'],
                                'index': block['index'],
                                'transaction': block['transaction'],
                                'proof': block['proof'],
                                'transactions': [OrderedDict([('sender',tx['sender']),
                                                        ('recipient',tx['recipient']),
                                                        ('amount',tx['amount'])]) for tx in block['transaction']]
                }
                updated_blockchain.append(updated_block)

            blockchain=updated_blockchain

            #transactions updated
            open_transcations = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transcations:
                updated_transaction =OrderedDict([('sender',tx['sender']),
                                                        ('recipient',tx['recipient']),
                                                        ('amount',tx['amount'])])
                updated_transactions.append(updated_transaction)
            open_transcations = updated_transactions

    except (IOError,ValueError,IndexError) :
        print("file not found so we initialize the blockchain with the genesis block")
        genesis_block = {
            'previous_hash': "",
            'index': 0,
            'transaction': [],
            'proof': 0
        }
        blockchain = [genesis_block]
        open_transcations = []
    finally:
        print('CleanUp!!')



load_data()

def save_data():
    try:
        with open('blockchain.txt','w') as f :
            f.write(json.dumps(blockchain))
            f.write('\n')
            f.write(json.dumps(open_transcations))
    except IOError:
        print('Saving Error!!')





def add_transaction(recipient, amount, sender=owner):
    """ Append a new value as well as the last blockchain value  to the blockchain

     Arguments:
         :sender : the sender of the coins.
         :recipient: the recipient of the coins.
         :amount: the amount of coins sent with the transcations (default =1.0)

    """


    transaction = OrderedDict([('sender',sender),
                               ('recipient',recipient),
                               ('amount',amount)])

    if verify_transaction(transaction):
        open_transcations.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True

    return False


def valid_proof(transaction, last_block, proof):
    guess = (str(transaction) + str(last_block) + str(proof)).encode()
    guess_hash = hash_string_256(guess)

    return guess_hash[0:2] == '00'


#calculation the Nonce numbre
def proof_of_work():
     last_block = blockchain[-1]
     last_hash  = hash_block(last_block)
     proof = 0

     while not valid_proof(open_transcations,last_hash,proof):
         proof +=1

     return proof


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    proof = proof_of_work()



    reward_transaction = OrderedDict([('sender','MINING'),
                                      ('recipient',owner),
                                      ('amount',MINING_REWARD)])
    # for reason of invalid transaction so ther is no reward so must make a copy the open_transactions
    # if we cant mine a block
    copied_transactions = open_transcations[:]
    copied_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transaction': copied_transactions,
        'proof':proof
    }

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


def verify_chain():
    """ verify the current blockchain and return true if the blockchain is valid"""

    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue

        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transaction'][:-1],block['previous_hash'],block['proof']):
            print("Proof of work is invalid !!")
            return False

    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transcations])




while True:
    print("Please choose")
    print("1.Add a new transaction value ")
    print("2.Mine a new block")
    print("3.output paricipants")
    print("4.Output the blockchain blocks ")
    print("5.check transactions validity")
    print("h.Manipulate the chain")
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
        print(participants)
    elif user_choice == '4':
        print_blockchain_elements()
    elif user_choice == '5':
        if verify_transactions():
            print("all transactions are valid")
        else:
            print("there are invalid transactions")
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': "",
                'index': 0,
                'transaction': [{"sender": "hatem", "recipient": "fraj", "amount": 100}]
            }

    elif user_choice == 'q':
        break
    else:
        print("Wrong input value, Please pick a value from te list")

    if not verify_chain():
        print_blockchain_elements()
        print("invalid blockchain!")
        break
    print('Balance of {} is : {:6.2f} '.format("hatem", get_balance('hatem')))
print('Done!')
