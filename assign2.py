#!/usr/bin/env python3

from Crypto.Cipher import AES

BLOCKSIZE = (128 // 8)

key_CBC = bytes.fromhex('140b41b22a29beb4061bda66b6747e14')
ct1_CBC = bytes.fromhex('4ca00ff4c898d61e1edbf1800618fb28'
                        '28a226d160dad07883d04e008a7897ee'
                        '2e4b7465d5290d0c0e6c6822236e1daa'
                        'fb94ffe0c5da05d9476be028ad7c1d81')
ct2_CBC = bytes.fromhex('5b68629feb8606f9a6667670b75b38a5'
                        'b4832d0f26e1ab7da33249de7d4afc48'
                        'e713ac646ace36e872ad5fb8a512428a'
                        '6e21364b0c374df45503473c5242a253')

key_CTR = bytes.fromhex('36f18357be4dbd77f050515c73fcf9f2')
ct1_CTR = bytes.fromhex('69dda8455c7dd4254bf353b773304eec'
                        '0ec7702330098ce7f7520d1cbbb20fc3'
                        '88d1b0adb5054dbd7370849dbf0b88d3'
                        '93f252e764f1f5f7ad97ef79d59ce29f'
                        '5f51eeca32eabedd9afa9329')
ct2_CTR = bytes.fromhex('770b80259ec33beb2561358a9f2dc617'
                        'e46218c0a53cbeca695ae45faa8952aa'
                        '0e311bde9d4e01726d3184c34451')

def xorbytes(b1, b2):
    return b''.join([bytes([b1[i] ^ b2[i]]) for i in range(min(len(b1), len(b2)))])

def decrypt_CBC(key, ciphertext):
    iv = ciphertext[0:BLOCKSIZE]
    plaintext = bytes()

    cipher = AES.new(key, AES.MODE_ECB)

    for i in range(BLOCKSIZE, len(ciphertext), BLOCKSIZE):
        plaintext += xorbytes(iv, cipher.decrypt(ciphertext[i:i+BLOCKSIZE]))
        iv = ciphertext[i:i+BLOCKSIZE]
    return plaintext[0:-plaintext[-1]]

def decrypt_CTR(key, ciphertext):
    iv = ciphertext[0:BLOCKSIZE]
    plaintext = bytes()
    ctr = 0
    
    cipher = AES.new(key, AES.MODE_ECB)
    
    for i in range(BLOCKSIZE, len(ciphertext), BLOCKSIZE):
        keystream = cipher.encrypt(iv[0:-1]+bytes([iv[-1]+ctr]))
        plaintext += xorbytes(keystream, ciphertext[i:i+BLOCKSIZE])
        ctr += 1
    return plaintext

print(decrypt_CBC(key_CBC, ct1_CBC))
print(decrypt_CBC(key_CBC, ct2_CBC))
print(decrypt_CTR(key_CTR, ct1_CTR))
print(decrypt_CTR(key_CTR, ct2_CTR))

