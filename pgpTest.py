import gnupg

gpg = gnupg.GPG(homedir="gpg")

def gen_key():
    print("Creating new key...")
    key_settings = gpg.gen_key_input(key_type='RSA', key_length=1024, key_usage='ESCA', passphrase="iotrocks")
    key = gpg.gen_key(key_settings)

    print("Exporting key to file...")
    out = gpg.export_keys(key.fingerprint)
    fl = open("public.key", "w")
    fl.write(out)
    fl.close()
    print("Key created and exorted successfully.")

    return key

#gen_key()

key = gpg.list_keys(secret=True)[-1]
print(gpg.list_keys(secret=True))
print(key['fingerprint'])

#out = gpg.export_keys(key['fingerprint'], secret=True)
#print(str(out))

message="Yay iot! wootwootwootwoot!"
encrypted = str(gpg.encrypt(message, key['fingerprint']))
print(encrypted)

decrypted = gpg.decrypt(str(encrypted), passphrase="iotrocks")
#ecrypted = gpg.decrypt_file("crypt", passphrase="iotrocks")
print(str(decrypted))

print(decrypted.ok)
print(decrypted.status)
