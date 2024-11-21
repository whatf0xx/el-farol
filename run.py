from typing import List
from bar import Guest
import matplotlib.pyplot as plt
from random import random


NO_GUESTS = 400
NO_CONNECTIONS = 5
STARTING_HAPPINESS_THRESHOLD = 0.9


def rand_bool() -> bool:
    return random() > STARTING_HAPPINESS_THRESHOLD


def initialise_guests(n: int, k: int) -> List[Guest]:
    global DEBUG_COUNTER
    guests = []
    for i in range(k):
        guest = Guest(i, guests.copy(), rand_bool())
        for pre in guests:
            pre.neighbours.append(guest)
        guests.append(guest)

    for i in range(k, n):
        neighbours = guests[i - k : i]
        guest = Guest(i, neighbours, rand_bool())
        for pre in guests[i - k : i]:
            pre.neighbours.append(guest)
        guests.append(guest)

    for i in range(k):
        guests[i].neighbours.extend(guests[-(k - i) :].copy())
        for j in range(-(k - i), 0):
            guests[j].neighbours.append(guests[i])

    return guests


def get_group_happiness(guests: List[Guest]) -> int:
    return sum(guest.happy for guest in guests)


def night(guests: List[Guest]) -> int:
    attendees = [guest for guest in guests if guest.decide()]
    attendance = len(attendees)
    for guest in attendees:
        guest.evaluate_evening(attendance)

    return attendance


if __name__ == "__main__":
    guests = initialise_guests(NO_GUESTS, NO_CONNECTIONS)

    attendance, group_happiness = zip(
        *[(night(guests), get_group_happiness(guests)) for _ in range(100)]
    )

    plt.figure()
    plt.plot(attendance)
    plt.title("Attendance")

    plt.figure()
    plt.plot(group_happiness)
    plt.title("Group happiness")

    plt.show()
