from flask import Flask, request, jsonify
from cipher.transposition import TranspositionCipher

app = Flask(__name__)
transposition_cipher = TranspositionCipher()

@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext')
    key = int(data.get('key'))
    if plaintext is None or key is None:
        return jsonify({'error': 'Missing plaintext or key'}), 400
    ciphertext = transposition_cipher.encrypt(plaintext, key)
    return jsonify({'ciphertext': ciphertext})

@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    data = request.get_json()
    ciphertext = data.get('ciphertext')
    key = int(data.get('key'))
    if ciphertext is None or key is None:
        return jsonify({'error': 'Missing ciphertext or key'}), 400
    plaintext = transposition_cipher.decrypt(ciphertext, key)
    return jsonify({'plaintext': plaintext})

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)