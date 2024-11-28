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
        decision = self.opinion + peer_pressure * neighbour_opinion
        if decision > 0:
            return True
        else:
            self.opinion += opinion_recovery if self.opinion < 0 else 0
            return False


class Simulation:
    def __init__(
        self,
        n: int,
        k: int,
        bad_evening_multiplier: float,
        max_capacity: int,
        attendance_sensitivity: float,
        peer_pressure: float,
        opinion_recovery: float,
    ):
        graph = nx.random_regular_graph(k, n)
        guests = {node: Guest(id=str(node)) for node in graph.nodes()}

        for node1, node2 in graph.edges():
            guests[node1].neighbours.append(guests[node2])
            guests[node2].neighbours.append(guests[node1])

        self.bad_evening_multiplier = bad_evening_multiplier
        self.max_capacity = max_capacity
        self.attendance_sensitivity = attendance_sensitivity
        self.peer_pressure = peer_pressure
        self.opinion_recovery = opinion_recovery
        self.guests = list(guests.values())

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
