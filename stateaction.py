class State:
    def __init__(self, name, reword=0, term=False):
        self.name = name
        self.reword = reword
        self.term = term

    def setTerm(self, reword=1):
        self.term = True
        self.reword = 1

    def __str__(self):
        return self.name


class Action:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class StateAction:
    def __init__(self, state, action, score=0, nextState=None):
        self.state = state
        self.action = action
        self.score = score
        self.nextState = nextState

    def __str__(self):
        return '{}, {}'.format(str(self.state), str(self.action))
