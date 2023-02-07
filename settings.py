import os
import dotenv

dotenv.load_dotenv('.env')

MASTER_PW_HASH = os.environ['MASTER_PW_HASH']
# KEY to be used for encryption/decryption
KEY = os.environ["KEY"].encode().decode('unicode_escape').encode("raw_unicode_escape")

# Database Credentials
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ.get('DB_PORT', '5432')
