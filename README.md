
# 🔐 Password Manager

- Console app for offline password management

## ✨ Technologies

* Python
* PostgreSQL

## Functionality

- One *MASTER* password to get in (**Argon2** hashed)
- Add, edit, delete, show by id, list all, list all containing some text
- Storing **URL, username and password**
- Passwords encrypted with AES-256 (GCM Mode)
    - 32-bytes KEY is used for encryption/decryption
- Uses auto **generated password** if no password was passed
- Checking if passwords are compromised (**haveibeenpwned's API**)
- Asking to confirm deleting a record / using compromised password
- Generated password **copied to clipboard** when chosen
---
- *MASTER* password and encryption *KEY* stored in the **.env** file and loaded as environment variables

## Dependencies

- **argon2**: Hashing algorithm
- **psycopg2**: PostgreSQL client for Python
- **pycryptodome**: Cryptography functions
- **python-dotenv**: Loads environment variables by reading them from a .env file
- **requests**: HTTP library

Install them all using:

```bash
  pip install -r requirements.txt
```
## Environment Variables

To run this project, you need to have the following environment variables to the **.env** file

`MASTER_PW_HASH`,
`KEY`

`DB_HOST`,
`DB_NAME`,
`DB_USER`,
`DB_PASSWORD`

## Screenshots

![CLI](https://github.com/georgievm/py-pw-manager/blob/1fa535f6539b92ed82c565bf044c069cf32c137f/readme-media/cli.PNG)

![DB_RECORD](https://github.com/georgievm/py-pw-manager/blob/1fa535f6539b92ed82c565bf044c069cf32c137f/readme-media/db_record.PNG)

## Improving it
- Make better CLI (use the ***click*** package)
- Store KEY in **.bin** file
- Use the prepared *logger.py* to implement logging and save all logs to a **.log** file
- Ability to change MASTER password
- Exception Handling for the execution of SQL
- New KEY to be generated using *PBKDF2* (password + salt needed)

## 📝 License

This project is *GPL v3* licensed.
