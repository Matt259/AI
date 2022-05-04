from userDB import db


def password_match(pwd,pwdR):
    if pwd==pwdR:
        return True
    else:
        return False

def check_empty_reg(username,email,pwd,pwdR):
    if username and email and pwd and pwdR:
        return True
    else:
        return False

def check_matching_data(username,email):
  pass

def register_user(username,email,pwd):
    if db:
        print("connected")


