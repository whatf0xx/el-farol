import matplotlib.pyplot as plt
from simulation import Simulation
from tqdm.contrib.itertools import product
import numpy as np


NIGHTS = 400
SHOW_LAST = 100
NO_GUESTS = 300
NO_CONNECTIONS = 11
MAX_CAPACITY = 60
PEER_PRESSURE = 1.18
BAD_EVENING_MULTIPLIER = 1.16
ATTENDANCE_SENSITIVITY = 0.5
OPINION_RECOVERY = 0.48


if __name__ == "__main__":
    peer_pressures = np.linspace(0.8, 1.4, 20)
    bad_eve_multipliers = np.linspace(1.0, 4.0, 20)
    opinion_recoveries = np.linspace(0.05, 0.5, 20)
    best_score = -np.inf
    params = (None, None, None)
    for p, b, r in product(
        peer_pressures, bad_eve_multipliers, opinion_recoveries
    ):
        sim = Simulation(
            NO_GUESTS,
            NO_CONNECTIONS,
            b,
            MAX_CAPACITY,
            ATTENDANCE_SENSITIVITY,
            p,
            r,
        )

        attendance, group_happiness = zip(*[sim.step() for _ in range(NIGHTS)])
        score = sum(group_happiness[-SHOW_LAST:])
        if score > best_score:
            best_score = score
            params = (p, b, r)

    p, b, r = params
    print(
        f"PEER_PRESSURE = {p}, BAD_EVENING_MULTIPLIER = {b}, OPINION_RECOVERY = {r}"
    )

    sim = Simulation(
        NO_GUESTS,
        NO_CONNECTIONS,
        b,
        MAX_CAPACITY,
        ATTENDANCE_SENSITIVITY,
        p,
        r,
    )

    attendance, group_happiness = zip(*[sim.step() for _ in range(NIGHTS)])
    score = sum(group_happiness[-SHOW_LAST:])

    plt.figure()
    plt.plot(attendance[-SHOW_LAST:])
    plt.title("Attendance")

    plt.figure()
    plt.plot(group_happiness[-SHOW_LAST:])
    plt.title("Group happiness")

    plt.show()
