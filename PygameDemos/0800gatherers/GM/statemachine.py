
class StateMachine():
    def __init__(self, actor, currentState, previousState = None):
        self.actor = actor
        self.currentState = currentState
        self.previousState = previousState
        self.currentState.enter(self.actor)

    def update(self):
        self.currentState.update(self.actor)

    def ChangeState(self, newstate):
        self.previousState = self.currentState
        self.currentState.exit(self.actor)
        self.currentState = newstate
        self.currentState.enter(self.actor)

    def RevertToPreviousState(self):
        self.ChangeState(self.previousState,self.actor)

class State():
    """State: an abstract superclass for all states.
    Documents the methods a state must support:
       Enter, Update, Exit
    These should be overridden as needed.
    """
    def __init__(self):
        pass
    def enter(self,actor):
        pass
    def update(self,actor):
        pass
    def exit(self,actor):
        pass
    
