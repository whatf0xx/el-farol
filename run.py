from typing import List
import matplotlib.pyplot as plt
import numpy as np
from random import random
import networkx as nx


NIGHTS = 800
SHOW_LAST = 100
NO_GUESTS = 300
NO_CONNECTIONS = 3
MAX_CAPACITY = 60
PEER_PRESSURE = 0.9
BAD_EVENING_MULTIPLIER = 2.0
ATTENDANCE_SENSITIVITY = 0.5
OPINION_RECOVERY = 0.21


class Guest:
    def __init__(
        self,
        id: int,
        neighbours: List["Guest"] | None = None,
        starting_opinion: float | None = None,
    ):
        self.id = id
        self.neighbours = neighbours if neighbours is not None else []
        self.opinion = (
            starting_opinion
            if starting_opinion is not None
            else 2 * (random() - 0.5)
        )

    def __repr__(self) -> str:
        return f"Guest{self.id}"

    def evaluate_evening(self, attendance: int):
        x = BAD_EVENING_MULTIPLIER
        c = MAX_CAPACITY
        s = ATTENDANCE_SENSITIVITY
        a = attendance
        self.opinion = x / (1 + np.exp((a - c) * s)) - x + 1

    def decide(self) -> bool:
        neighbour_opinion = sum(n.opinion for n in self.neighbours)
        decision = self.opinion + PEER_PRESSURE * neighbour_opinion
        if decision > 0:
            return True
        else:
            self.opinion += OPINION_RECOVERY
            return False


def initialise_guests(n: int, k: int) -> List[Guest]:
    graph = nx.random_regular_graph(k, n)
    guests = {node: Guest(id=str(node)) for node in graph.nodes()}
    # nx.draw(
    #     graph,
    #     with_labels=True,
    #     node_color="lightblue",
    #     edge_color="gray",
    #     node_size=500,
    # )
    # plt.show()
    for node1, node2 in graph.edges():
        guests[node1].neighbours.append(guests[node2])
        guests[node2].neighbours.append(guests[node1])

    return list(guests.values())


def night(guests: List[Guest]) -> int:
    # print(f"{guests[50]}; opinion: {guests[50].opinion}")
    # for n in guests[50].neighbours:
    #     print(f"\t{n}; opinion: {n.opinion}")
    attendees = [guest for guest in guests if guest.decide()]
    attendance = len(attendees)
    for guest in attendees:
        guest.evaluate_evening(attendance)

    happiness = sum(guest.opinion for guest in guests)

    return attendance, happiness


if __name__ == "__main__":
    guests = initialise_guests(NO_GUESTS, NO_CONNECTIONS)

    attendance, group_happiness = zip(*[night(guests) for _ in range(NIGHTS)])

    plt.figure()
    plt.plot(attendance[-SHOW_LAST:])
    plt.title("Attendance")

    plt.figure()
    plt.plot(group_happiness[-SHOW_LAST:])
    plt.title("Group happiness")

    plt.show()
