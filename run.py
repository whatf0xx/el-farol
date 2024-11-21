from typing import List
from bar import Guest
import matplotlib.pyplot as plt
from random import random


def rand_bool() -> bool:
    return random() > 0.4


def initialise_guests(n: int) -> List[Guest]:
    guest0 = Guest(0, [], rand_bool())

    guest1 = Guest(1, [guest0], rand_bool())
    guest0.neighbours.append(guest1)

    guest2 = Guest(2, [guest1], rand_bool())
    guest1.neighbours.append(guest2)

    guests = [guest0, guest1, guest2]
    for i in range(3, n):
        neighbours = [guests[i - 1]]
        if i % 2 == 0:  # if even
            neighbours.append(guests[i - 3])

        guest = Guest(i, neighbours, rand_bool())
        guests.append(guest)

        guests[i - 1].neighbours.append(guest)
        if i % 2 == 0:
            guests[i - 3].neighbours.append(guest)

    guests[-3].neighbours.append(guest0)
    guests[-1].neighbours.extend([guest0, guest2])
    guest0.neighbours.extend([guests[-1], guests[-2]])
    guest2.neighbours.append(guests[-2])

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
    guests = initialise_guests(100)
    # nights = range(100)
    # attendance = []
    # group_happiness = []
    # for _ in nights:
    #     attendance.append(night(guests))
    #     group_happiness.append(get_group_happiness(guests))

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
