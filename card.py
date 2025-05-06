TEMPURA = "tempura"
SASHIMI = "sashimi"
DUMPLING = "dumpling"
DOUBLE_MAKI = "double_maki"
TRIPLE_MAKI = "triple_maki"
SINGLE_MAKI = "single_maki"
SALMON = "salmon"
SQUID = "squid"
EGG = "egg"
PUDDING = "pudding"
WASABI = "wasabi"
CHOPSTICKS = "chopsticks"

class Card(object):
    def __init__(self, name):
        self.name = name
        # Used to define a set of cards. If there is no previous, then it's head of stack.
        self.next = None

    def __str__(self):
        if self.next:
            return  str(f"{self.name} + {self.next.name}")
        return str(self.name)
    def __repr__(self):
        if self.next:
            return  str(f"{self.name} + {self.next.name}")
        return str(self.name)