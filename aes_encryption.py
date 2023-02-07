from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from settings import KEY

def generate_key() -> bytes:
    return get_random_bytes(32) # 256-bit


def encrypt(plain_pw, key=KEY) -> tuple:
    """
    Args:
        plain_pw (str): Password to be encrypted
        key (bytes): used to encrypt text
    
    Returns:
        tuple: Consisting of encrypted text, nonce and auth_tag
    """
    cipher = AES.new(key, AES.MODE_GCM)

    ciphertext, auth_tag = cipher.encrypt_and_digest(plain_pw.encode())
    nonce = cipher.nonce

    return ciphertext, nonce, auth_tag


def decrypt(ciphertext, nonce, auth_tag, key=KEY) -> str:
    """
    Args:
        ciphertext (bytes): encrypted text
        nonce (bytes): the random number used to encrypt
        auth_tag (bytes): the auth code used for verification
        key (bytes): used to decrypt text
    
    Returns:
        str: Original password
    """
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plain_pw_bytes = cipher.decrypt_and_verify(ciphertext, auth_tag)

    return plain_pw_bytes.decode()

# Test it out
def main():
    print(f'KEY: {KEY}, {type(KEY)}')
    encrypted, nonce, auth_tag = encrypt('mypass')

    print(f'Encr: {encrypted}, {type(encrypted)}')
    print(f'Nonce: {nonce}, {type(nonce)}')
    print(f'Auth_tag: {auth_tag}, {type(auth_tag)}')

    decrypted = decrypt(encrypted, nonce, auth_tag)
    print(f'Decr: {decrypted}, {type(decrypted)}')

if __name__ == '__main__':
    main()
