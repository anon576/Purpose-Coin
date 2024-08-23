from flask import Flask, request, jsonify
import requests
import socket
from goverment import Government

class Node:
    def __init__(self, port, blockchain, registration_server_url):
        self.ip = self.get_ip_address()  # Automatically get the actual IP address
        self.port = port
        self.blockchain = blockchain
        self.government = Government(blockchain)
        self.registration_server_url = registration_server_url
        self.app = Flask(__name__)
        self.setup_routes()
        self.register_with_server()

    def get_ip_address(self):
        """ Automatically get the device's actual IP address. """
        # Use a socket to find the actual IP address of the machine
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connect to an external host; this doesn't have to be reachable
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
        except Exception:
            ip_address = '127.0.0.1'  # Fallback to localhost if unable to get IP
        finally:
            s.close()
        return ip_address

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
            # Avoid rebroadcasting the block back to the sender
            if self.blockchain.validateBlock(block):
                self.blockchain.chain.append(block)
                self.broadcast_block(block)  # Continue broadcasting to other nodes
            return jsonify({'message': 'Block broadcasted!'}), 200

        @self.app.route('/get_chain', methods=['GET'])
        def get_chain():
            return jsonify({'chain': self.blockchain.chain}), 200

        # Updated route to handle /add_pending_organization with correct parameters
        @self.app.route('/add_pending_organization', methods=['POST'])
        def add_pending_organization():
            data = request.get_json()
            org_id = data.get('org_id')
            org_name = data.get('org_name')
            
            if not org_id or not org_name:
                return jsonify({'message': 'Organization ID and name required!'}), 400
            
            # Register organization using the correct method from Blockchain class
            self.blockchain.registerOrganization(org_id, org_name)
            return jsonify({'message': 'Organization added!'}), 200

        @self.app.route('/approve_organization', methods=['POST'])
        def approve_organization():
            data = request.get_json()
            org_id = data.get('org_id')
            if org_id:
                if self.government.approveOrganization(org_id):
                    return jsonify({'message': f'Organization {org_id} approved successfully!'}), 200
                else:
                    return jsonify({'message': 'Organization not found in pending list.'}), 404
            return jsonify({'message': 'Invalid data!'}), 400

        @self.app.route('/execute_transaction', methods=['POST'])
        def execute_transaction():
            data = request.get_json()
            sender = data.get('sender')
            recipient = data.get('recipient')
            amount = data.get('amount')
            category = data.get('category')
            if sender and recipient and amount and category:
                self.execute_transaction(sender, recipient, amount, category)
                return jsonify({'message': 'Transaction executed!'}), 200
            return jsonify({'message': 'Invalid transaction data!'}), 400
        
        @self.app.route('/pending_transaction', methods=['POST'])
        def pending_transaction():
            data = request.get_json()
            sender = data.get('sender')
            recipient = data.get('recipient')
            amount = data.get('amount')
            category = data.get('category')
            if sender and recipient and amount and category:
                self.add_pending_transaction(sender, recipient, amount, category)
                return jsonify({'message': 'Transaction added to pending list!'}), 200
            return jsonify({'message': 'Invalid transaction data!'}), 400
        

    def execute_transaction(self, sender, recipient, amount, category):
        # Logic to validate and execute transaction
        if sender not in self.blockchain.users or recipient not in self.blockchain.users:
            print("Sender or recipient not found.")
            return

        if not self.blockchain.isValidCategory(category):
            print(f"Invalid category: {category}")
            return

        sender_user = self.blockchain.users[sender]
        recipient_user = self.blockchain.users[recipient]

        if sender_user['category'] != category:
            print(f"Sender's category does not match transaction category.")
            return

        # Create and add the transaction
        self.blockchain.newTransaction(sender, recipient, amount)

        # Print transaction for verification
        print(f"Transaction added: {sender} -> {recipient}, Amount: {amount}, Category: {category}")

    def add_pending_transaction(self, sender, recipient, amount, category):
        """ Add transaction to pending list if valid """
        if sender not in self.blockchain.users or recipient not in self.blockchain.users:
            print("Sender or recipient not found.")
            return

        if not self.blockchain.isValidCategory(category):
            print(f"Invalid category: {category}")
            return

        sender_user = self.blockchain.users[sender]
        recipient_user = self.blockchain.users[recipient]

        if sender_user['category'] != category:
            print(f"Sender's category does not match transaction category.")
            return

        # Create and add the transaction
        self.blockchain.newTransaction(sender, recipient, amount)

        # Print transaction for verification
        print(f"Transaction added to pending list: {sender} -> {recipient}, Amount: {amount}, Category: {category}")

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
        print(f"Starting node server at {self.ip}:{self.port}")
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


def run_node(port, blockchain, registration_server_url):
    node = Node(port, blockchain, registration_server_url)
    node.start_server()
