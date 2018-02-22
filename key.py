from iota import *
import gnupg

node = "http://iota.teamveno.eu:14265"
seed = "FZVHIPWMPGSEUTFZMEVSMPUXZWMKLNRAEMYKKUTU9DFQIK99UKYPAZVGVCNHRYHAIETUI" #Not actually used when sending.
api = Iota(node, seed)

address = "YBYCJDOFGODBLMDXDSOO9PYUH9DRLROBXPKHAGAYRD9ZKZ9HKAIWFDQJVTEDVFQHKLOQXQPAKPETS9FHC"

gpg = gnupg.GPG(homedir="gpg")

def get_key(name):
    for k in gpg.list_keys():
        if k['uids'][0].split(" ")[0] == name:
            return k
    return False

def send_message(tag, msg):
    tx = ProposedTransaction(address=Address(address), value=0, tag=Tag(tag), message=TryteString.from_unicode(msg))
    api.send_transfer(depth = 100, transfers=[tx])

def encrypt_message(enc_key, sign_key, msg):
    out = str(gpg.encrypt(msg, enc_key['fingerprint'], default_key=sign_key['fingerprint']))
    #sign = str(gpg.sign(msg, default_key=sign_key['fingerprint']))
    #print(sign)
    return out

key = get_key("key")
lock = get_key("lock")
print(key)
print(lock)

#print(encrypt_message("open"))
msg = encrypt_message(lock, key, "open")
print(msg)
send_message(b'IOT', msg)
