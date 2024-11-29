from typing import List
from random import random
import numpy as np
import networkx as nx


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

    def evaluate_evening(
        self,
        attendance: int,
        bad_evening_multiplier: float,
        max_capacity: int,
        attendance_sensitivity: float,
    ) -> float:
        x = bad_evening_multiplier
        c = max_capacity
        s = attendance_sensitivity
        a = attendance
        self.opinion = x / (1 + np.exp((a - c) * s)) - x + 1
        return self.opinion

    def decide(self, peer_pressure: float, opinion_recovery: float) -> bool:
        neighbour_opinion = sum(n.opinion for n in self.neighbours)
        decision = (
            self.opinion
            + peer_pressure * neighbour_opinion
            + 0.1 * (random() - 0.5)
        )
        if decision > 0:
            return True
        else:
            self.opinion = min(0, self.opinion + opinion_recovery)
            return False


def _init_clustered(n: int, k: int) -> List[Guest]:
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


def _init_random_regular(n: int, k: int) -> List[Guest]:
    graph = nx.random_regular_graph(k, n)
    guests = {node: Guest(id=str(node)) for node in graph.nodes()}

    for node1, node2 in graph.edges():
        guests[node1].neighbours.append(guests[node2])
        guests[node2].neighbours.append(guests[node1])

    return list(guests.values())


class Simulation:
    graph_types = {
        "clustered": _init_clustered,
        "random_regular": _init_random_regular,
    }

    def __init__(
        self,
        n: int,
        k: int,
        graph_type: str | None = "random_regular",
        bad_evening_multiplier: float = 1.0,
        max_capacity: int = 60,
        attendance_sensitivity: float = 0.5,
        peer_pressure: float = 1.0,
        opinion_recovery: float = 0.1,
    ):
        self.bad_evening_multiplier = bad_evening_multiplier
        self.max_capacity = max_capacity
        self.attendance_sensitivity = attendance_sensitivity
        self.peer_pressure = peer_pressure
        self.opinion_recovery = opinion_recovery
        self.guests = self.graph_types[graph_type](n, k)

    def step(self) -> int:
        p, r = self.peer_pressure, self.opinion_recovery
        attendees = [guest for guest in self.guests if guest.decide(p, r)]
        attendance = len(attendees)

        b, m, a = (
            self.bad_evening_multiplier,
            self.max_capacity,
            self.attendance_sensitivity,
        )
        for guest in attendees:
            guest.evaluate_evening(attendance, b, m, a)

        happiness = sum(guest.opinion for guest in self.guests)

        return attendance, happiness
