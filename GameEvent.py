class Calendar:
    def __init__(self, events):
        self.events = events

    def begin(self):
        self.turn=0

    def next_turn(self):
        self.turn += 1
        return self.events[self.turn-1]

    def get_length(self):
        return len(self.events)

class GameEvent:
    def __init__(self):
        pass

    def run(self, game_object):
        pass
