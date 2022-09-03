def calc(function):
    def operator(*args):
        print(function.__name__)
        return function(*args)
    return operator

@calc
def add(n1, n2):
    return n1 + n2

print(add(7,32))
