import hashlib
import json
from time import time
from urllib.parse import urlparse
from config import difficulty
import requests

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactionsPool = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash=1, proof=1)

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactionsPool,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.transactionsPool = []

        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.transactionsPool.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

    
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading <number of difficulty> zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = "".join([str(last_proof),str(proof),last_hash]).encode()
        #guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == "0" * difficulty

    @property
    def last_block(self):
        return self.chain[-1]

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """
        
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            
            # log for debug
            print ("      ┌─────────────────────────────────────────┐")
            print ("      │        last_block           begins      │")
            print ("──────┴─────────────────────────────────────────┴──────")
            print (last_block)
            print ("──────┬─────────────────────────────────────────┬──────")
            print ("      │        last_block           ends        │")
            print ("      └─────────────────────────────────────────┘")

            print ("      ┌─────────────────────────────────────────┐")
            print ("      │        index: " + str(current_index))
            print ("      └─────────────────────────────────────────┘")

            print ("      ┌─────────────────────────────────────────┐")
            print ("      │        block                begins      │")
            print ("──────┴─────────────────────────────────────────┴──────")
            print (last_block)
            print ("──────┬─────────────────────────────────────────┬──────")
            print ("      │        block                ends        │")
            print ("      └─────────────────────────────────────────┘")


            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], self.hash(last_block)):
                return False

            last_block = block
            current_index += 1

        return True


    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        #print (str(self.nodes))
        
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)
        print ("self.chain length: " + str(max_length))

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get('http://' + node + '/chain')
            print ("response.status_code: " + str(response.status_code))

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                print ("node length: " + str(length))
                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            print ("self.chain:" + str(self.chain))
            return True

        return False