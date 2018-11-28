from random import choice, randint
import string

class myclass:
    def __init__(self):
        # generate 50k random attributes
        N = 10
        for k in range(50000):
            setattr(self,
                   choice(string.ascii_uppercase)+\
                   ''.join(choice(string.ascii_uppercase + string.digits) \
                           for _ in range(N)), randint(1,1000))

c = myclass()
