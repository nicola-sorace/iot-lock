import gnupg

gpg = gnupg.GPG(homedir="gpg")

def gen_key(name):
    print("Creating new key...")
    key_settings = gpg.gen_key_input(name_real=name, key_type='RSA', key_length=1024, key_usage='ESCA', passphrase="iotrocks")
    key = gpg.gen_key(key_settings)

    print("Exporting key to file...")
    out = gpg.export_keys(key.fingerprint)
    fl = open("public.key", "w")
    fl.write(out)
    fl.close()
    print("Key created and exported successfully.")

    return key

#gen_key("lock")
#gen_key("key")

#key = gpg.list_keys(secret=True)[-1]
#print(gpg.list_keys(secret=True))

def get_key(name):
    for k in gpg.list_keys():
        if k['uids'][0].split(" ")[0] == name:
            return k
    return False

key = get_key("key")
lock = get_key("lock")

#out = gpg.export_keys(key['fingerprint'], secret=True)
#print(str(out))

message="Yay iot! wootwootwootwoot!"
encrypted = gpg.encrypt(message, lock['fingerprint'], default_key=key['fingerprint'])
print(str(encrypted))


decrypted = gpg.decrypt(str(encrypted), passphrase="iotrocks")
#ecrypted = gpg.decrypt_file("crypt", passphrase="iotrocks")
print(str(decrypted))

verify = gpg.verify(str(encrypted)).valid
print(verify)

#print(decrypted.ok)
#print(decrypted.status)
