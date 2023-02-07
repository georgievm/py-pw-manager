import requests
from Crypto.Hash import SHA1


def get_api_response(first5) -> object:
    """
    Args:
        first5 (str): First 5 characters of the SHA-1 password hash
    """
    url = 'https://api.pwnedpasswords.com/range/' + first5
    response = requests.get(url)

    if (code := response.status_code) != 200:
        raise RuntimeError(f'API call unsuccessful: HTTP ERROR {code}')

    return response


def get_hash(password) -> tuple:
    hash = SHA1.new(password.encode()).hexdigest().upper()
    first5, tail = hash[:5], hash[5:]

    return first5, tail


def check(password: str) -> int:
    """
    Args:
        password (str): Plain password
    Returns:
        (int): Number of times the password has been seen before
    """
    pw_first5, pw_tail = get_hash(password)
    response = get_api_response(pw_first5)

    splitted = (line.split(':') for line in response.text.splitlines())
    for tail, count in splitted:
        if pw_tail == tail:
            return count
    return 0


def main():
    try:
        print(check('password'))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
