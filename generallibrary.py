import os

def rel(*x):
    return os.path.join(os.path.dirname(__file__),  *x).replace('\\','/')
