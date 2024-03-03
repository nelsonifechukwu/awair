from cryptography.fernet import Fernet
class Password:
    def __init__(self,key = None):
        if key is None:
            self._key = Fernet.generate_key()
            self._key = self._key.decode()
        else:
            self._key = key
    @property
    def key(self):
        return self._key
    
    def encrypt_password(self, password):
        key = self.key
        encrypt_key = key.encode()
        encrypted_pass = Fernet(encrypt_key).encrypt(password.encode())
        encrypted_pass = encrypted_pass.decode()
        return key, encrypted_pass
    def decrypt_password(self, encrypted):
        key = self.key
        key = key.encode()
        password = encrypted.encode()
        decrypted_pass = Fernet(key).decrypt(password)
        return decrypted_pass.decode()
