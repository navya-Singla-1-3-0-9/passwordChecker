import requests
import hashlib
import sys


def read_response(hashes, check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    print(hashes)
    for h, count in hashes:
        if h == check:
            return count
    return 0


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(f'error fetching: {res.status_code},check the api and try again')
    return res


def pwned_api_check(password):
    # check if password is in api response
    sha1pw = hashlib.sha1(password.encode('utf=8')).hexdigest().upper()
    first5, tail = sha1pw[:5], sha1pw[5:]
    response = request_api_data(first5)
    return read_response(response, tail)


def main(pw):
    count = pwned_api_check(pw)
    if count:
        print(f'YOUR PASSWORD HAS BEEN HACKED {count} TIMES')

    else:
        print('YOUR PASSWORD IS SECURE')


main(input())
