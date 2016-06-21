class Calendar:
    def __init__(self, events):
        self.events = events

    def begin(self):
        self.turn=0

    def next_turn(self):
        if self.turn == 0:
            self.turn = 1
            return self.events[0]
        else:
            self.turn += 1
            return self.events[self.turn-1]

    def get_length(self):
        return len(self.events)

class GameEvent:
    def __init__(self):
        pass

    def run(self, game_object):
        pass

# test script
if __name__ == "__main__":
    calendar = Calendar(["One", "Two", "Three"])
    calendar.begin()
    print calendar.next_turn()
    print calendar.next_turn()
    print calendar.next_turn()
