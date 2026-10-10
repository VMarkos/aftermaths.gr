class MultiSet(list):
    def __init__(self, ls):
        list.__init__(self, ls)
        self.ls = ls
    
    def __eq__(self, other):
        if not len(self.ls) == len(other.ls):
            return False
        for x in self.ls:
            if not x in other.ls:
                return False
        return True

    def __add__(self, other):
        return MultiSet(self.ls + other.ls)