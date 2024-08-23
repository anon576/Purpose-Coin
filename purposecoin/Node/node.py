from flask import Flask, request, jsonify
import requests
import threading

class Node:
    def __init__(self, port, blockchain):
        self.port = port
        self.blockchain = blockchain
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/new_block', methods=['POST'])
        def new_block():
            data = request.get_json()
            block = data.get('block')
            if self.blockchain.validateBlock(block):
                self.blockchain.chain.append(block)
                self.blockchain.pendingTransaction = []
                return jsonify({'message': 'Block added to the blockchain!'}), 200
            else:
                return jsonify({'message': 'Invalid block!'}), 400

        @self.app.route('/broadcast_block', methods=['POST'])
        def broadcast_block():
            data = request.get_json()
            block = data.get('block')
            # Broadcast block to all connected nodes (excluding self)
            # This can be expanded with actual network communication
            return jsonify({'message': 'Block broadcasted!'}), 200

        @self.app.route('/get_chain', methods=['GET'])
        def get_chain():
            return jsonify({'chain': self.blockchain.chain}), 200

    def start_server(self):
        self.app.run(port=self.port)

    def broadcast_block(self, block):
        # Implement the logic to send the block to other nodes
        import requests
        # Example URL, should be replaced with actual nodes' addresses
        url = f'http://localhost:5000/broadcast_block'
        payload = {'block': block}
        requests.post(url, json=payload)

def run_node(port, blockchain):
    node = Node(port, blockchain)
    node.start_server()
