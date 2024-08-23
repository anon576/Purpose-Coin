from flask import Flask, request, jsonify
import requests

class Node:
    def __init__(self, ip, port, blockchain, registration_server_url):
        self.ip = ip
        self.port = port
        self.blockchain = blockchain
        self.registration_server_url = registration_server_url
        self.app = Flask(__name__)
        self.setup_routes()
        self.register_with_server()

    def setup_routes(self):
        @self.app.route('/new_block', methods=['POST'])
        def new_block():
            data = request.get_json()
            block = data.get('block')
            if self.blockchain.validateBlock(block):
                self.blockchain.chain.append(block)
                self.blockchain.pendingTransaction = []
                self.broadcast_block(block)  # Broadcast the new block to other nodes
                return jsonify({'message': 'Block added to the blockchain!'}), 200
            else:
                return jsonify({'message': 'Invalid block!'}), 400

        @self.app.route('/broadcast_block', methods=['POST'])
        def broadcast_block():
            data = request.get_json()
            block = data.get('block')
            # Broadcast block to all connected nodes (excluding self)
            self.broadcast_block(block)
            return jsonify({'message': 'Block broadcasted!'}), 200

        @self.app.route('/get_chain', methods=['GET'])
        def get_chain():
            return jsonify({'chain': self.blockchain.chain}), 200

    def register_with_server(self):
        payload = {'ip': self.ip, 'port': self.port}
        try:
            response = requests.post(f'{self.registration_server_url}/register_node', json=payload)
            if response.status_code == 200:
                print(f"Node registered successfully: {response.json()}")
            else:
                print(f"Failed to register node: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error registering node: {e}")

    def start_server(self):
        self.app.run(host=self.ip, port=self.port)

    def broadcast_block(self, block):
        try:
            # Fetch the list of nodes from the registration server
            response = requests.get(f'{self.registration_server_url}/get_nodes')
            if response.status_code == 200:
                nodes = response.json().get('nodes', [])
                for node in nodes:
                    node_ip = node.get('ip')
                    node_port = node.get('port')
                    if node_ip != self.ip or node_port != self.port:  # Avoid sending to self
                        url = f'http://{node_ip}:{node_port}/broadcast_block'
                        payload = {'block': block}
                        try:
                            requests.post(url, json=payload)
                        except requests.exceptions.RequestException as e:
                            print(f"Error sending block to {node_ip}:{node_port}: {e}")
            else:
                print(f"Failed to fetch node list: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching node list: {e}")

def run_node(ip, port, blockchain, registration_server_url):
    node = Node(ip, port, blockchain, registration_server_url)
    node.start_server()
