from bar import Bar, Guest

if __name__ == "__main__":
    guest0 = Guest(0, [], True)

    guest1 = Guest(1, [guest0], True)
    guest0.neighbours.append(guest1)

    guest2 = Guest(2, [guest1], True)
    guest1.neighbours.append(guest2)

    guests = [guest0, guest1, guest2]
    for i in range(3, 100):
        neighbours = [guests[i - 1]]
        if i % 2 == 0:  # if even
            neighbours.append(guests[i - 3])

        guest = Guest(i, neighbours, False)
        guests.append(guest)

        guests[i - 1].neighbours.append(guest)
        if i % 2 == 0:
            guests[i - 3].neighbours.append(guest)

    guest0.neighbours.append([guests[-1], guests[-2]])
    guest2.neighbours.append(guests[-2])

    for i in range(10):
        print(f"{guests[i]}, neighbours: {guests[i].neighbours}")
