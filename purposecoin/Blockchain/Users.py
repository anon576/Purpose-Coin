

class User:
    def __init__(self, user_id, blockchain):
        self.user_id = user_id
        self.blockchain = blockchain

    def receiveFunds(self, amount):
        # Assume funds are received through transactions initiated by lending organizations
        print(f'User {self.user_id} has received {amount}.')
