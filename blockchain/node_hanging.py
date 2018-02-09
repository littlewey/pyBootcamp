from blockchain import Blockchain
from wallet import Wallet
from flask import Flask, jsonify, request
from config import miningReward

# Instantiate the Node
app = Flask(__name__)

# Instantiate the Wallet
wallet = Wallet()


# Instantiate the Blockchain
blockchain = Blockchain()

# endpoints

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender = "0",
        recipient = wallet.address,
        amount = miningReward
    )
    print ("start mining...")
    # Create the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Created",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200



@app.route('/transactions', methods=['GET'])
def all_transactions():
    response = {
        'transactions': blockchain.transactionsPool,
        'length': len(blockchain.transactionsPool),
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(k in values for k in required):
        return 'Missing values', 400

    sender    = values['sender']
    recipient = values['recipient'] 
    amount    = values['amount']
    signature = values['signature']


    if not wallet.verification(sender, recipient, amount, signature):
        return 'Signature verification failure', 401

    # Create a new Transaction
    blockchain.new_transaction(sender, recipient, amount,)
    transactionIndex = blockchain.last_block['index'] + 1
    response = {'message': 'Transaction will be added to Block %d' %transactionIndex }
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/secret', methods=['GET'])
def get_secret():
    response = {
        'message': "secret sent in console..."
    }
    secret = wallet.secret
    print ("      ┌─────────────────────────────────────────┐")
    print ("      │        secret base64 output begins      │")
    print ("──────┴─────────────────────────────────────────┴──────")
    print (secret)
    print ("──────┬─────────────────────────────────────────┬──────")
    print ("      │        secret base64 output ends        │")
    print ("      └─────────────────────────────────────────┘")

    return jsonify(response), 200

@app.route('/nodes', methods=['GET'])
def all_nodes():
    response = {
        'nodes': blockchain.nodes,
        'length': len(blockchain.nodes),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)