from blockchain import Blockchain
from node import run_node
import threading

def main():
    blockchain = Blockchain()
    registration_server_url = 'http://192.168.137.113:5000'  # Replace with actual URL
    ports = [5000, 5001, 5002]  # Example ports for different nodes

    for port in ports:
        threading.Thread(target=run_node, args=(port, blockchain, registration_server_url)).start()

if __name__ == '__main__':
    main()
