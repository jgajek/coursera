#!/usr/bin/env python3

from Crypto.Hash import SHA256
import os
import binascii

FILENAME="bday.mp4"

def getblock(f):
    for offset in reversed(range(0, os.path.getsize(FILENAME), 1024)):
        f.seek(offset)
        yield f.read(1024)

f = open(FILENAME, "rb")
h = bytes()

for b in getblock(f):
    h = SHA256.new(b + h).digest()

print(binascii.hexlify(h))
