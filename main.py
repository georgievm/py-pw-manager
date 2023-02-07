from settings import MASTER_PW_HASH
from argon2_hash import verify_hash
from aes_encryption import encrypt, decrypt
from pwnedpasswords import check
from getpass import getpass
from password_gen import gen_password
from database import Database
# from logger import get_logger
import subprocess

class PM:
    def __init__(self):
        self.print_ascii_art()
        # Check DB connection
        try:
            db = Database()
        except Exception as e:
            self.logger.error('Unable to connect to database!')
            print(f'Unable to connect!\n{e}')
            exit()
        else:
            # Try to get IN
            if verify_hash(MASTER_PW_HASH, getpass("Master Password: ")):
                self.db = db
                self.show_menu()
                self.start_choosing()
            else:
                print('Authentication failed!')
                exit()
    
    def handle_add(self):
        url = self.complete_url(input('URL: '))
        username = input('Username: ')

        if not (url and username):
            print('Empty input(s)!')
            return
        
        default_pw = gen_password()
        plain_pw = input(f'Password [{default_pw}]: ')
        if not plain_pw:
            plain_pw = default_pw
            subprocess.run('xclip', universal_newlines=True, input=plain_pw)
        
        # Check if pw has been seen in data breach
        try:
            seen = check(plain_pw)
        except Exception as e:
            pass
        else:
            if seen:
                print(f'WARNING: This password has been seen {int(seen):,} times before!')
                if not self.ask_to_continue('Add'):
                    print('Cancelled.')
                    return
            
        encr_pw, nonce, auth_tag = encrypt(plain_pw)
        self.db.add_record(url, username, encr_pw, nonce, auth_tag)

    def handle_delete(self, record_id):
        record = self.db.get_record(record_id)

        if record:
            print(f'Record... {self.format_record(record)}')
            if self.ask_to_continue():
                self.db.del_record(record_id)
            else:
                print('Cancelled.')
        else:
            print('No such record.')
    
    def handle_edit(self, record_id):
        record = self.db.get_record(record_id)

        if not record:
            print('No such record.')
            return
        
        # get current values
        url, username, encr_pw, nonce, auth_tag = record[1:]
        plain_pw = decrypt(encr_pw, nonce, auth_tag)

        # get new values
        new_url = input(f'URL [{url}]: ')
        new_username = input(f'Username [{username}]: ')
        new_plain_pw = input(f'Password [{plain_pw}]: ')

        # set to old ones if empty
        new_url = url if not new_url else self.complete_url(new_url)
        new_username = username if not new_username else new_username
        new_plain_pw = plain_pw if not new_plain_pw else new_plain_pw

        # Case: Nothing is changed
        if (new_url, new_username, new_plain_pw) == (url, username, plain_pw):
            print('Nothing to update.')
            return

        # Check if pw has been seen in data breach
        if times_seen:=is_pwned(plain_pw):
            print(f'WARNING: This password has been seen {int(times_seen):,} times before!')
            
            if not self.ask_to_continue('Update'):
                print('Cancelled.')
                return
        
        # Case: Password not changed -> update only URL & username
        if new_plain_pw == plain_pw:
            sql = """
                UPDATE records
                SET url = %(url)s, username = %(usr)s
                WHERE record_id = %(id)s;
            """
        # Update everything
        else:
            encr_pw, nonce, auth_tag = encrypt(new_plain_pw)
            sql = """
                UPDATE records
                SET url=%(url)s, username=%(usr)s, encr_pw=%(pw)s, nonce=%(nonce)s, auth_tag=%(tag)s
                WHERE record_id = %(id)s;
            """
        
        params = {
            'id': record_id,
            'url': new_url,
            'usr': new_username,
            'pw': encr_pw,
            'nonce': nonce,
            'tag': auth_tag
        }
        self.db.execute(sql, params)
        print('Updated!')

    def handle_show(self, record_id):
        record = self.db.get_record(record_id)

        if record:
            print(self.format_record(record))
        else:
            print('No such record.')

    def handle_show_all(self):
        records = self.db.get_all()
        if not records:
            print('Nothing out there :(')
            return

        for record in records:
            print(self.format_record(record))

    def handle_show_containing(self, text):
        records = self.db.get_all()

        if not records:
            print('You need to have some records first!')
            return
        count = 0

        for record in records:
            record_id, url, username, encr_pw, nonce, auth_tag = record
            plain_pw = decrypt(encr_pw, nonce, auth_tag)

            if text in url or text in username or text in plain_pw:
                count += 1
                print(self.format_record(record))

    def print_ascii_art(self):
        print()
        with open('ascii_art.txt', 'r') as f:
            for line in f.readlines():
                print(line, end='')
        print()
    
    def show_menu(self):
        menu = """
            (0) Show Menu
            (1) Add New
            (2) Edit Record By ID
            (3) Delete Record By ID
            (4) Show Record by ID
            (5) Show All Containing...
            (6) Show All
            (Q) Quit
            """
        print(menu)
    
    def ask_to_continue(self, msg='Continue') -> bool:
        return input(f"{msg} [Y/N]: ").lower() == 'y'
    
    def start_choosing(self):
        done = False

        while not done:
            choice = input(': ').lower()
            match choice:
                case '0':
                    self.show_menu()
                case '1':
                    self.handle_add()
                case '2':
                    self.handle_edit(input('ID: '))
                case '3':
                    self.handle_delete(input('ID: '))
                case '4':
                    self.handle_show(input('ID: '))
                case '5':
                    self.handle_show_containing(input('Text: '))
                case '6':
                    self.handle_show_all()
                case 'q':
                    self.db.close()
                    exit()
                case other:
                    print('Invalid Choice!')

            print('-'*40)
    
    def complete_url(self, url):
        if not url.startswith('http'):
            url = 'https://' + url
        return url
    
    def format_record(self, record):
        # encr_pw, nonce, auth_tag are now of type memoryview!
        record_id, url, username, encr_pw, nonce, auth_tag = record
        plain_pw = decrypt(bytes(encr_pw), bytes(nonce), bytes(auth_tag))

        return f"[{record_id}] {url:}, {username}, {plain_pw}"

def main():
    pm = PM()

main()
