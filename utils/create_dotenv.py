content = """
MASTER_PW_HASH = "$argon2id$v=19$m=65536,t=3,p=4$3QKbU0cLQGX13JWbFB2a5Q$vLABhVdDhyMxN3lDiXuVj7ZC6fyXLZbotaz1naJnVJU"
KEY = '\xe9\xf8/\xd31\xde\xc9:W%G[\xaf\xc0\xf7\x80"\nOT\x04@\x07So\x8aL:\xbe\xeaFX'
DB_HOST = "localhost"
DB_NAME = "pw_manager"
DB_USER = "postgres"
DB_PASSWORD = "password"
"""

try:
    with open('../.env', 'w') as f:
        f.write(content)
except Exception as e:
    print(e)
else:
    print('.env file created')
