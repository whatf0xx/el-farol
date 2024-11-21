from typing import List
import matplotlib.pyplot as plt
from random import random
from networkx import random_regular_graph, draw


NIGHTS = 800
SHOW_LAST = 100
NO_GUESTS = 20
NO_CONNECTIONS = 5
MAX_CAPACITY = 60
PEER_PRESSURE = 0.9


class Guest:
    def __init__(
        self, id: int, neighbours: List["Guest"], starting_opinion: float
    ):
        self.id = id
        self.neighbours = neighbours
        self.opinion = starting_opinion

    def __repr__(self) -> str:
        return f"Guest{self.id}"

    def evaluate_evening(self, attendance: int, capacity: int):
        if attendance > capacity:
            self.opinion = -1.0
        else:
            self.opinion = 1.0

    def decide(self, peer_pressure: float) -> bool:
        neighbour_opinion = sum(n.opinion for n in self.neighbours)
        decision = self.opinion + peer_pressure * neighbour_opinion
        if decision > 0:
            return True
        else:
            self.opinion += 0.1
            return False


def initialise_guests(n: int, k: int) -> List[Guest]:
    global DEBUG_COUNTER
    guests = []
    for i in range(k):
        guest = Guest(i, guests.copy(), random())
        for pre in guests:
            pre.neighbours.append(guest)
        guests.append(guest)

    for i in range(k, n):
        neighbours = guests[i - k : i]
        guest = Guest(i, neighbours, random())
        for pre in guests[i - k : i]:
            pre.neighbours.append(guest)
        guests.append(guest)

    for i in range(k):
        guests[i].neighbours.extend(guests[-(k - i) :].copy())
        for j in range(-(k - i), 0):
            guests[j].neighbours.append(guests[i])

    return guests


def night(guests: List[Guest]) -> int:
    # print(f"{guests[50]}; opinion: {guests[50].opinion}")
    # for n in guests[50].neighbours:
    #     print(f"\t{n}; opinion: {n.opinion}")
    attendees = [guest for guest in guests if guest.decide(PEER_PRESSURE)]
    attendance = len(attendees)
    for guest in attendees:
        guest.evaluate_evening(attendance, MAX_CAPACITY)

    return attendance, attendance * int(attendance < MAX_CAPACITY)


if __name__ == "__main__":
    guests = initialise_guests(NO_GUESTS, NO_CONNECTIONS)

    # attendance, group_happiness = zip(*[night(guests) for _ in range(NIGHTS)])

    # plt.figure()
    # plt.plot(attendance[-SHOW_LAST:])
    # plt.title("Attendance")

    # plt.figure()
    # plt.plot(group_happiness[-SHOW_LAST:])
    # plt.title("Group happiness")
    graph = random_regular_graph(NO_CONNECTIONS, NO_GUESTS)
    degrees = [degree for _, degree in graph.degree()]
    print("Degrees of nodes:", degrees)
    draw(
        graph,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=500,
    )
    plt.show()

    plt.show()
