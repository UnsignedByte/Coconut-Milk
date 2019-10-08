import os
import sys

_keyfile = "Data/keys/key.txt"

if not os.path.exists(_keyfile):
    print("Missing bot key");
    sys.exit();

def readKey():
    return open(_keyfile, 'r').read().strip()

_keyvalue = None

def key():
    global _keyvalue

    if not _keyvalue:
        return readKey()
    else:
        return _keyvalue
