#!/usr/bin/env python

import urllib2
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:
            #print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding

#iv = 'f20bdba6ff29eed7b046d1df9fb70000'.decode('hex')
#iv = '58b1ffb4210a580f748b4ac714c001bd'.decode('hex')
iv = '4a61044426fb515dad3f21f18aa577c0'.decode('hex')

ciphertext = [
     '58b1ffb4210a580f748b4ac714c001bd',
     '4a61044426fb515dad3f21f18aa577c0',
     'bdf302936266926ff37dbf7035d5eeb4'
]

plaintext = [chr(0)] * 16
po = PaddingOracle()

def getmask(i, c):
    pad = chr(0) * i + chr(16 - i) * (16 - i)
    guess = chr(0) * i + chr(c) + ''.join(plaintext[i+1:16])
    return strxor(pad, guess)

def strxor(a, b):
    return ''.join([chr(ord(a[i]) ^ ord(b[i])) for i in range(len(a))])

for i in reversed(range(16)):
    print "Guessing at position %d" % i
    for c in range(2, 256):
        if po.query(strxor(iv, getmask(i, c)).encode('hex') + ciphertext[2]):
            print "Correct guess: %d" % (c)
            plaintext[i] = chr(c)
            break

print ''.join(plaintext)
