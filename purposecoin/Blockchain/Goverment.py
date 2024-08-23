


class Government:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def registerCategory(self, category, is_valid):
        self.blockchain.categories[category] = is_valid
    
    def isValidCategory(self, category):
        return self.blockchain.categories.get(category, False)
    
    def verifyAndRegisterOrganization(self, org_id, org_name):
        # In a real system, additional verification logic would be added here
        self.blockchain.registerOrganization(org_id, org_name)
        print(f'Lending Organization {org_id} applied for registration.')
    
    def approveOrganization(self, org_id):
        self.blockchain.approveOrganization(org_id)
