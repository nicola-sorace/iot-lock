rasp = False  #Set to False to debug on non-raspberryPi computer

from iota import *
#import gnupg
if rasp:
    import RPi.GPIO as GPIO
import time
import hashlib
import pysftp

### Setup connection to the IOTA network:
node = "http://iota.teamveno.eu:14265"  #TODO Automatic node selection.
seed = "FZVHIPWMPGSEUTFZMEVSMPUXZWMKLNRAEMYKKUTU9DFQIK99UKYPAZVGVCNHRYHAIETUI"
api = Iota(node, seed)
#print(api.get_node_info())
#print(api.get_new_addresses(index=0, count=1)['addresses'])

### Setup PGP encryption:
#gpg = gnupg.GPG(homedir="gpg")

### Setup Raspberry Pi I/O pins:
if rasp:
    GPIO.setmode(GPIO.BCM)
    pinA = 5
    pinB = 6
    GPIO.setup(pinA, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pinB, GPIO.OUT, initial=GPIO.LOW)
else:
    con = pysftp.Connection('172.20.146.217', username='pi', password='marty')

def turn_lock(dir):  #Physically turns the lock. dir=0: close, dir=1: open
        delay = 1  #Seconds to turn for.
        if rasp:
            if dir==1:
                a = pinA
                b = pinB
            else:
                a = pinB
                b = pinA
            GPIO.output(b, False)
            GPIO.output(a, True)
            time.sleep(delay)
            GPIO.output(a, False)
        else:
            if dir==1:
                con.execute("python open.py")
            else:
                con.execute("python close.py")

def get_bundles(n=None):  #Get all messages from the IOTA network:
        return api.get_transfers(start=n).get(u'bundles')

def print_messages(ms):  #Print raw messages (does not decrypt):
        for m in ms:
                for tx in m:
                        print(TryteString.decode(tx.signature_message_fragment))

def interpret_message(m):  #Decrypts and executes instruction:
        tx = m[0]
        raw = TryteString.decode(tx.signature_message_fragment)
        '''
        msg = str(gpg.decrypt(raw, passphrase="iotrocks"))

        verify = gpg.verify(raw).valid
        print("signature validity:")
        print(verify)
        '''

        msg = raw.split(",")
        tstamp = msg[0]
        name = msg[1]
        token = msg[2]
        cmd = msg[3]

        time_difference = int(time.time()) - int(tstamp)
        print("token:")
        print(token)
        if token==str(hashlib.sha256(str.encode(tstamp+name+"password")).hexdigest()):
            if time_difference <= 120 and not(time_difference < 0):
                if cmd=="open" or True:
                        print("User \'"+name+"\' is opening lock.")
                        turn_lock(1)
                elif cmd=="close":
                        print("User \'"+name+"\' is closing lock.")
                        turn_lock(0)
                else:
                        print("Unrecognized instruction: "+cmd)
            else:
                print("Timestamp is too far off ("+str(time_difference)+").")
        else:
            print("Invalid token.")


def listen_loop():  #Continuously checks the IOTA network for new instructions:
    ms = get_bundles()
    n = len(ms)
    print("Found", n, "old message(s).")
    print("------------------------")

    print("Waiting for new messages:")
    while(True):
        ms = get_bundles()  #TODO This is a bottleneck
        if len(ms)==n:
            print("No new messages")
        else:
            print("Received", len(ms)-n, "new message(s) [decrypted]:")
            interpret_message(ms[-1])
            n = len(ms)

listen_loop()
