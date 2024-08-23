from purposecoin.Blockchain.Blockchain import Blockchain
from purposecoin.Node.Node import run_node
import threading

def main():
    blockchain = Blockchain()
    registration_server_url = 'http://192.168.137.113:5000'  # Replace with actual registration server URL
    ip_address = '0.0.0.0'  # Bind to all available interfaces
    ports = [5000, 5001, 5002]  # Example ports for different nodes

    # Create and start a node on each specified port in a separate thread
    for port in ports:
        threading.Thread(target=run_node, args=(ip_address, port, registration_server_url, blockchain)).start()

if __name__ == '__main__':
    main()
