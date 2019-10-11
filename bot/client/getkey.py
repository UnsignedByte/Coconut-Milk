import os
import sys

def readKey():
    if not os.path.exists("Data/keys/key.txt"):
        return [os.environ['DISCORD_KEY'], os.environ['IMGUR_KEY'], os.environ['WOLFRAMALPHA_KEY']]
    return [open("Data/keys/key.txt", 'r').read().strip(),
            open("Data/keys/imgurkey.txt", 'r').read().strip(),
            open("Data/keys/wolframalphakey.txt", 'r').read().strip()]
