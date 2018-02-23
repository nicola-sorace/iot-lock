from iota import *
#import gnupg
import hashlib

import time

node = "http://iota.teamveno.eu:14265"
seed = "FZVHIPWMPGSEUTFZMEVSMPUXZWMKLNRAEMYKKUTU9DFQIK99UKYPAZVGVCNHRYHAIETUI" #Not actually used when sending.
api = Iota(node, seed)

address = "YBYCJDOFGODBLMDXDSOO9PYUH9DRLROBXPKHAGAYRD9ZKZ9HKAIWFDQJVTEDVFQHKLOQXQPAKPETS9FHC"

#gpg = gnupg.GPG(homedir="gpg")

'''
def get_key(name):
    for k in gpg.list_keys():
        if k['uids'][0].split(" ")[0] == name:
            return k
    return False
'''

def send_message(tag, msg):
    tx = ProposedTransaction(address=Address(address), value=0, tag=Tag(tag), message=TryteString.from_unicode(msg))
    api.send_transfer(depth = 100, transfers=[tx])

def get_message(name, password, cmd):
    '''
    out = str(gpg.encrypt(msg, enc_key['fingerprint'], default_key=sign_key['fingerprint']))
    sign = str(gpg.sign(msg, default_key=sign_key['fingerprint']))
    #print(sign)
    '''
    tstamp = str(int(time.time()))
    
    msg = tstamp+","+name+","+str(hashlib.sha256(str.encode(tstamp+name+password)).hexdigest())+","+cmd
    return msg

'''
key = get_key("key")
lock = get_key("lock")
print(key)
print(lock)
'''

#print(encrypt_message("open"))
msg = get_message("user1", "password", "open")
print(msg)
send_message(b'IOT', msg)
