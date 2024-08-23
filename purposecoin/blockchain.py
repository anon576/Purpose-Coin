import json
import random
import hashlib as h
from datetime import datetime

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pendingTransaction = []
        self.organizations = {}
        self.users = {}
        self.categories = {}
        print('Creating a genesis block')
        self.newBlock(nonce="0000")

    def newBlock(self, nonce=None):
        if self.chain:
            previousHash = self.chain[-1]['blockHash']
        else:
            previousHash = None

        block = {
            'index': len(self.chain) + 1,
            'timestamp': datetime.utcnow().isoformat(),
            'transaction': self.pendingTransaction,
            'previousHash': previousHash,
            'nonce': nonce or format(random.getrandbits(64), "x"),
        }
        sthash = json.dumps(block, sort_keys=True)
        blockHash = self.hash(sthash)
        block['blockHash'] = str(blockHash)
        
        self.pendingTransaction = []
        
        return block

    @staticmethod
    def hash(block):
        return h.sha256(block.encode()).hexdigest()
    
    @property
    def lastBlock(self):
        return self.chain[-1] if self.chain else None

    def newTransaction(self, sender, recipient, amount):
        self.pendingTransaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

    def proofOfWork(self):
        nonce = 0
        while True:
            block = self.newBlock(nonce)
            if self.validHash(block):
                self.chain.append(block)
                self.pendingTransaction = []
                self.broadcast_block(block)
                print(f'Found new block: {block}')
                break
            nonce += 1

    @staticmethod
    def validHash(block):
        return block['blockHash'].startswith('0000')

    def validateBlock(self, block):
        if self.chain and block['previousHash'] != self.lastBlock['blockHash']:
            return False
        return self.validHash(block)
    
    def validateChain(self):
        for i in range(1, len(self.chain)):
            if not self.validateBlock(self.chain[i]):
                return False
        return True

    def registerOrganization(self, org_id, org_name):
        
        self.organizations[org_id] = {
            'name': org_name,
            'status': 'pending'
        }
    
    def approveOrganization(self, org_id):
        if org_id in self.organizations:
            org = self.organizations.pop(org_id)
            org['status'] = 'approved'
            self.organizations[org_id] = org

    def registerUser(self, user_id, user_name):
        self.users[user_id] = {
            'name': user_name
        }
    
    def broadcastUpdatedOrganizations(self):
        # Placeholder for broadcasting updated list of organizations to all nodes
        print('Broadcasting updated organizations to all nodes.')

    def isValidCategory(self, category):
        return self.categories.get(category, False)
