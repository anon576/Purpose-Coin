import json
import random
import hashlib as h
from datetime import datetime


class Blockchain:
    def __init__(self):
        self.chain=[]
        self.pendingTransaction=[]
        print('Creating a genesis block')
        self.newBlock()
        
    def newBlock(self):
        if(self.chain):
            previousHash = self.chain[len(self.chain)-1]['blockHash']
        else:
            previousHash = None
        block = {
            'index': len(self.chain) + 1,
            'timestamp': datetime.utcnow().isoformat(),
            'transaction': self.pendingTransaction,
            'previousHash': previousHash,
            'nonce': format(random.getrandbits(64), "x"),
        }
        sthash = json.dumps(block, sort_keys=True)  # Sort keys for consistent hashing
        blockHash = self.hash(sthash)
        block['blockHash'] = str(blockHash)
        
        return block

      
    @staticmethod  
    def hash(block):
        return h.sha256(block.encode()).hexdigest()
    @property 
    def lastBlock(self):
        return self.chain[-1] if self.chain else None
        
    def newTransaction(self,sender,recipent,amount):
        self.pendingTransaction=({
        'sender':sender,
        'recipent':recipent,
        'amount':amount})
        
     
     
    def proofOfWork(self):
        while True:
            newBlock=self.newBlock()
            if self.validHash(newBlock):
                break
                
        self.chain.append(newBlock)
        print(f'Found new block {newBlock}')
        
    @staticmethod   
    def validHash(block):
        return block['blockHash'].startswith('0000')
     
        