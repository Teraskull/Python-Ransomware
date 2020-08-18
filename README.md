# Python-Ransomware

To test the Ransomware on your machine:

* Edit lines 49 and 140 in the `RansomWare.py` file with your own absolute paths. For testing purposes you can use the `localRoot` directory.

* **[ATTACKER]** Run the `RSA_private_public_keys.py` script to generate two keys: a private and public key.

* **[TARGET]** Run the ransomware script - localRoot `.txt` files will be encrypted now.

* **[ATTACKER]** Run the `Decrypt_fernet_key.py` script to decrypt the `EMAIL_ME.txt` file (will be on your desktop), this will give you a `PUT_ME_ON_DESKtOP.txt` file. Once you put this on the desktop, the ransomware will decrypt the `localRoot` files in that directory.

#### Disclaimer

> This tool is only for testing and academic purposes and can only be used where strict consent has been given. Do not use it for
> illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. Developers assume no
> liability and are not responsible for any misuse or damage caused by this tool and software in general.
