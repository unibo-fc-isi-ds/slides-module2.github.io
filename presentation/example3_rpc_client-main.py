from snippets.lab4.example0_users import gc_user, gc_credentials_ok, gc_credentials_wrong
import sys


user_db = RemoteUserDatabase(address(sys.argv[1]))

# Trying to get a user that does not exist should raise a KeyError
try:
    user_db.get_user('gciatto')
except RuntimeError as e:
    assert 'User with ID gciatto not found' in str(e)

# Adding a novel user should work
user_db.add_user(gc_user)

# Trying to add a user that already exist should raise a ValueError
try:
    user_db.add_user(gc_user)
except RuntimeError as e:
    assert str(e).startswith('User with ID')
    assert str(e).endswith('already exists')

# Getting a user that exists should work
assert user_db.get_user('gciatto') == gc_user.copy(password=None)

# Checking credentials should work if there exists a user with the same ID and password (no matter which ID is used)
for gc_cred in gc_credentials_ok:
    assert user_db.check_password(gc_cred) == True

# Checking credentials should fail if the password is wrong
assert user_db.check_password(gc_credentials_wrong) == False