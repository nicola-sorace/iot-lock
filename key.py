from iota import *
import gnupg

node = "http://iota.teamveno.eu:14265"
seed = "FZVHIPWMPGSEUTFZMEVSMPUXZWMKLNRAEMYKKUTU9DFQIK99UKYPAZVGVCNHRYHAIETUI" #Not actually used when sending.
api = Iota(node, seed)

address = "YBYCJDOFGODBLMDXDSOO9PYUH9DRLROBXPKHAGAYRD9ZKZ9HKAIWFDQJVTEDVFQHKLOQXQPAKPETS9FHC"

gpg = gnupg.GPG(homedir="gpg")
key = gpg.list_keys(secret=True)[-1]  #The lock's public key

def send_message(tag, msg):
    tx = ProposedTransaction(address=Address(address), value=0, tag=Tag(tag), message=TryteString.from_unicode(msg))
    api.send_transfer(depth = 100, transfers=[tx])

def encrypt_message(msg):
    out = str(gpg.encrypt(msg, key['fingerprint']))
    return out

#print(encrypt_message("open"))
send_message(b'IOT', encrypt_message("open"))
