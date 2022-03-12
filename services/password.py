import hashlib

def get_hash_password(password):
    pass_with_sult = password + 'zXckd3!'
    hash = hashlib.sha256(pass_with_sult.encode('UTF-8')).hexdigest()
    return hash