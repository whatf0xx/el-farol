from typing import List


MAX_TIME_OFF = 5


class Bar:
    def __init__(self):
        self.guest_list = []

    def check_in(self, guest: "Guest"):
        self.guest_list.append(guest)

    def capacity(self) -> int:
        return len(self.guest_list)

    def reset(self):
        self.guest_list = []


class Guest:
    def __init__(
        self, id: int, neighbours: List["Guest"], starting_happy: bool
    ):
        self.id = id
        self.neighbours = neighbours
        self.happy = starting_happy
        self.days_since_visit = 0

    def __repr__(self) -> str:
        return f"Guest{self.id}"

    def visit(self, bar: Bar):
        bar.check_in(self)

    def evaluate_evening(self, bar: Bar):
        if bar.capacity > 60:
            self.happy = False
        else:
            self.happy = True

    def decide(self) -> bool:
        if self.happy == 1:
            # if you went last night and it was good, go again
            return True

        # then last time we went was overcrowded. When do we try again?
        if self.days_since_last_visit == MAX_TIME_OFF:
            # go again because it's been so long, anyway
            self.days_since_visit = 0
            return True

        # in the middle, see what our friends think
        opinion_sum = sum(n.happy for n in self.neighbours)
        if opinion_sum > 0:
            # most your friends think you should go
            self.days_since_last_visit = 0
            return True
        else:
            # don't bother, wait another day
            self.days_since_last_visit += 1
            return False
