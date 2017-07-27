import random

from stateaction import State, Action, StateAction
from qtable import QTable


times = 50
learningRate = 0.9
discount = 0.8
jumpProb = 0.05
stateNum = 15


class reinforcementExample:
    def __init__(self):
        self.states = []
        self.actions = []
        self.qtable = None
        self.currentState = None
        self.currentAction = None

    def loadStates(self):
        self.states = [State(str(i)) for i in range(stateNum)]
        self.states[-1].setTerm()
        self.currentState = self.states[0]


    def loadActions(self):
        self.actions = [Action('left'), Action('right')]

    def loadQTable(self):
        self.qtable = QTable(self.states, self.actions, getNextState=self._getNextState)
        self.qtable[self.states[0], self.actions[0]].nextState = self.states[0]
        self.qtable[self.states[-1], self.actions[1]].nextState = self.states[-1]
        for key in self.qtable:

    def chooseAction(self, state=None):
        if state is None:
            state = self.currentState

        if random.random() < jumpProb:
            self.currentAction = random.choice(self.actions)
        else:
            self.currentAction = self._getBestStateAction(state).action

    def maxReword(self, state):
        if state is None:
            return 0
        elif state.term:
            return state.reword
        else:
            return self._getBestStateAction(state).score

    def nextState(self, state, action):
        try:
            return self.qtable[state, action].nextState
        except KeyError:
            return state

    def updateQTable(self, state, action, predictReword):
        stateAction = self.qtable[state, action]
        try:
            learnedValue = stateAction.nextState.reword
        except AttributeError:
            learnedValue = 0
        learnedValue += discount * predictReword - stateAction.score
        stateAction.score = stateAction.score + learningRate * learnedValue

    def next(self):
        self.currentState = self.nextState(self.currentState, self.currentAction)
        self.currentAction = None

    def _getBestStateAction(self, state):
        stateActions = self._getAllStateActions(state)
        bestScore = max(stateActions, key=lambda x: x.score).score
        bestStateActions = filter(lambda x:x.score == bestScore, stateActions)
        return random.choice(list(bestStateActions))

    def _getAllStateActions(self, state, action=None):
        if state is None:
            state = self.currentState
        return tuple(self.qtable[state, a] for a in self.actions)

    def _getNextState(self, state, action, states):
        if action.name == 'left':
            index =  states.index(state) - 1
        elif action.name == 'right':
            index =  states.index(state) + 1
        else:
            raise ValueError('wrong action')

        try:
            return states[index]
        except IndexError:
            return None


def main():
    rie = reinforcementExample()
    rie.loadStates()
    rie.loadActions()
    rie.loadQTable()
    for time in range(times):
        steps = 0
        rie.currentState = rie.states[0]
        while not rie.currentState.term:
            steps += 1
            rie.chooseAction()
            predictReword = rie.maxReword(rie.nextState(rie.currentState, rie.currentAction))
            rie.updateQTable(rie.currentState, rie.currentAction, predictReword)
            rie.next()
        print(f'{time}. End before running {steps} steps.')


if __name__ == '__main__':
    main()
