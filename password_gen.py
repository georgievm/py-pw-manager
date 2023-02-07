import string
import secrets


def gen_password(len=15):

    chars = string.ascii_letters + string.digits + string.punctuation

    new_password = ''
    for _ in range(len):
        new_password += secrets.choice(chars)

    return new_password

def main():
    print(gen_password())

if __name__ == '__main__':
    main()
