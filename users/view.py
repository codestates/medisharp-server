from . import users

@users.route('/')
def users_login():
    return "test"