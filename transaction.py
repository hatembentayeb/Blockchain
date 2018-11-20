from collections import OrderedDict
from utility.printable import Printable

class Transaction(Printable):
    """ a transaction whitch be added to a block in the block chain

        Attribute:
            :sender: the sender of the coins
            :recipient: the recipeient of the coins
            :signature: the signature of the transaction
            :amount: the amount of coins sent
    """
    def __init__(self, recipient, sender, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature




    def to_ordered_dict(self):
        return OrderedDict([('sender',self.sender),('recipient',self.recipient),('amount',self.amount)])
