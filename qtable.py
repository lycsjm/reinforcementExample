from stateaction import State, Action, StateAction


class QTable(dict):
    def __init__(self, states=None, actions=None, getNextState=None, *args,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.init(states, actions, getNextState)


    def init(self, states, actions, getNextState):
        for state in states:
            for action in actions:
                if getNextState is None:
                    nextState = None
                else:
                    nextState = getNextState(state, action, states)
                self[state, action] = StateAction(state, action, 0, nextState)
