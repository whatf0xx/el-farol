from typing import List
from bar import Guest


def initialise_guests(n: int) -> List[Guest]:
    guest0 = Guest(0, [], True)

    guest1 = Guest(1, [guest0], True)
    guest0.neighbours.append(guest1)

    guest2 = Guest(2, [guest1], True)
    guest1.neighbours.append(guest2)

    guests = [guest0, guest1, guest2]
    for i in range(3, n):
        neighbours = [guests[i - 1]]
        if i % 2 == 0:  # if even
            neighbours.append(guests[i - 3])

        guest = Guest(i, neighbours, False)
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
    print("Debug call to get_happiness")
    return sum(guest.happy for guest in guests)


def night(guests: List[Guest]) -> int:
    print("Debug call to night")
    attendees = [guest for guest in guests if guest.decide()]
    attendance = len(attendees)
    for guest in attendees:
        guest.evaluate_evening(attendance)

    return attendance


if __name__ == "__main__":
    guests = initialise_guests(100)
    for guest in guests[:10]:
        print(f"{guest}, neighbours: {guest.neighbours}")
    for guest in guests[90:]:
        print(f"{guest}, neighbours: {guest.neighbours}")
    # nights = range(100)
    # attendance = []
    # group_happiness = []
    # for _ in nights:
    #     attendance.append(night(guests))
    #     group_happiness.append(get_group_happiness(guests))

    # attendance, group_happiness = [
    #     (night(guests), get_group_happiness(guests)) for _ in range(10)
    # ]
