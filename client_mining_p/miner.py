import hashlib
import requests
import time

import sys


# TODO: Implement functionality to search for a proof

def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"

def proof_of_work(last_proof):
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1
    
    return proof


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        print('Searching for next proof')
        # TODO: Get the last proof from the server and look for a new one
        last_proof = requests.get('http://localhost:5000/last_proof').json()['last_proof']
        start = time.process_time()
        proof = proof_of_work(last_proof)
        # TODO: When found, POST it to the server {"proof": new_proof}
        miningResponse = requests.post('http://localhost:5000/mine', json={'proof': proof}).json()
        # TODO: If the server responds with 'New Block Forged'
        if miningResponse['message'] == "New Block Forged":
        # add 1 to the number of coins mined and print it.  
            coins_mined += 1
            print(f'Total coins mined: {coins_mined}')
            end = time.process_time()
            print(f'Mining operation took: {end - start} seconds')
        # Otherwise,
        else:
        # print the message from the server.
            print(miningResponse['message'])
        
