#unifor unique id
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet

class Node:

    def __init__(self):
        #self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        # initiliase the blockchain with public kye generated for the node (the sender id)
        self.blockchain = Blockchain(self.wallet.public_key)
    def get_transaction_value(self):
        """returns the input of the user (a new transaction amount) as a float"""

        tx_recipient = input("enter the recipeint of the transation : ")
        tx_amount = float(input('you tranction amount please: '))
        return tx_recipient, tx_amount


    def get_user_choice(self):
        return input("Your choice : ")


    def print_blockchain_elements(self):
        # output the blockchain list to the console
        for block in self.blockchain.chain:
            print("outputting blocks:")
            print(block)
        else:
            print("-" * 20)

    def listen_for_input(self):

        while True:
            print("Please choose")
            print("1.Add a new transaction value ")
            print("2.Mine a new block")
            print("3.Output the blockchain blocks ")
            print("4.check transactions validity")
            print("5.Create Wallet")
            print("6.Load Wallet")
            print("7.save keys")
            print("q.Quit")

            user_choice = self.get_user_choice()

            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data

                signature = self.wallet.sign_transaction(self.wallet.public_key,recipient,amount)

                if self.blockchain.add_transaction(recipient,self.wallet.public_key, signature, amount):
                    print("added transaction !")
                else:
                    print("transaction failed!")

                print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
                # mine a new block
                if not self.blockchain.mine_block():
                    print("Minig Block failed !, Got no Wallet ?")
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance()):
                    print("all transactions are valid")
                else:
                    print("there are invalid transactions")
            elif user_choice == '5':

                self.wallet.create_keys()
                #initiliase the blockchain with public kye generated for the node (the sender id)
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice =='6':
                self.wallet.load_key()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                break
            else:
                print("Wrong input value, Please pick a value from te list")


            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("invalid blockchain!")
                break
            print('Balance of {} is : {:6.2f} BTC'.format(self.wallet.public_key, self.blockchain.get_balance()))
        print('Done!')

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()