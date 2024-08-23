from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to hold registered nodes
registered_nodes = {}

@app.route('/register_node', methods=['POST'])
def register_node():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')
    
    if not ip or not port:
        return jsonify({'error': 'Invalid data'}), 400
    
    node_id = f"{ip}:{port}"
    
    if node_id in registered_nodes:
        return jsonify({'message': 'Node already registered'}), 200
    
    registered_nodes[node_id] = {'ip': ip, 'port': port}
    return jsonify({'message': 'Node registered successfully'}), 200

@app.route('/get_nodes', methods=['GET'])
def get_nodes():
    return jsonify({'nodes': list(registered_nodes.values())}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
