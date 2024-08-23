

class LendingOrganization:
    def __init__(self, org_id, blockchain):
        self.org_id = org_id
        self.blockchain = blockchain

    def requestFundsFromGovernment(self, amount, category):
        if self.org_id in self.blockchain.organizations and self.blockchain.organizations[self.org_id]['status'] == 'approved':
            if self.blockchain.isValidCategory(category):
                self.blockchain.newTransaction(sender='Government', recipient=self.org_id, amount=amount)
                self.blockchain.proofOfWork()  # Add block with the transaction
                print(f'Lending Organization {self.org_id} has requested {amount} from the government for category {category}.')
            else:
                print('Invalid category.')
        else:
            print('Organization not approved or not found.')
    
    def lendMoneyToUser(self, user_id, amount):
        if self.org_id in self.blockchain.organizations and self.blockchain.organizations[self.org_id]['status'] == 'approved':
            if user_id in self.blockchain.users:
                self.blockchain.newTransaction(sender=self.org_id, recipient=user_id, amount=amount)
                self.blockchain.proofOfWork()  # Add block with the transaction
                print(f'Lending Organization {self.org_id} has lent {amount} to User {user_id}.')
            else:
                print('User not found.')
        else:
            print('Organization not approved or not found.')
