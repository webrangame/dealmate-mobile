import hmac
import hashlib

salt = 'sp8UxnDKXAbQNr1WTcUtq4jiM2DsFSnK3rutoQA5fu0='
target = '832c18aca270e07e169cf8e03d605b550873147671d649114c95bcee0af75e06'

def hash_it(s):
    return hmac.new(salt.encode(), s.lower().strip().encode(), hashlib.sha256).hexdigest()

tests = [
    "57",
    "itranga@gmail.com",
    "itranga@gmai.com",
    "57@niyogen.com",
    "user_57",
    "itranga @gmail.com",
    "ranga",
    "itranga",
    "57",
    "57 ",
    " 57"
]

for t in tests:
    h = hash_it(t)
    print(f"'{t}' -> {h}")
    if h == target:
        print("MATCH FOUND!")

# Also try as integer
try:
    h = hash_it(str(57))
    print(f"str(57) -> {h}")
except: pass
