# government.py
from blockchain import Blockchain

class Government:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def approveOrganization(self, org_id):
        if org_id in self.blockchain.organizations:
            self.blockchain.approveOrganization(org_id)
            return True
        return False

    def approve_pending_user(self, user_id):
        if user_id in self.blockchain.pendingUsers:
            self.blockchain.approveUser(user_id)
            return True
        return False
