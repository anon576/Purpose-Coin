from purposecoin.Blockchain.Blockchain import Blockchain
from purposecoin.Node.Node import run_node
import threading

def main():
    blockchain = Blockchain()
    ports = [5000, 5001, 5002]  # Example ports for different nodes

    for port in ports:
        threading.Thread(target=run_node, args=(port, blockchain)).start()

if __name__ == '__main__':
    main()
