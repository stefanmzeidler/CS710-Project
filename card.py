class Card(object):
    CHOPSTICKS = "chopsticks"
    DOUBLE_MAKI = "double_maki"
    DUMPLING = "dumpling"
    EGG = "egg"
    PUDDING = "pudding"
    SALMON = "salmon"
    SASHIMI = "sashimi"
    SINGLE_MAKI = "single_maki"
    SQUID = "squid"
    TEMPURA = "tempura"
    TRIPLE_MAKI = "triple_maki"
    WASABI = "wasabi"
    def __init__(self, name):
        self.name = name
        # Used to define a set of cards. If there is no previous, then it's head of stack.
        self.next = None
        self.prev = None

    def __str__(self):
        if self.next:
            return  str(f"{self.name} + {self.next.name}")
        return str(self.name)
    def __repr__(self):
        if self.next:
            return  str(f"{self.name} + {self.next.name}")
        return str(self.name)