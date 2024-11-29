import matplotlib.pyplot as plt
from simulation import Simulation
from tqdm.contrib.itertools import product
import numpy as np


NIGHTS = 200
SHOW_LAST = 20
NO_GUESTS = 300
NO_CONNECTIONS = 11
MAX_CAPACITY = 60
PEER_PRESSURE = 0.97
BAD_EVENING_MULTIPLIER = 1.33
ATTENDANCE_SENSITIVITY = 0.5
OPINION_RECOVERY = 0.11


if __name__ == "__main__":
    peer_pressures = np.linspace(0.9, 1.2, 40)
    opinion_recoveries = np.linspace(0.05, 0.2, 40)
    bad_eve_multipliers = np.linspace(0.9, 3.0, 40)
    best_score = np.inf
    params = (None, None, None)
    for p, r, m in product(
        peer_pressures, opinion_recoveries, bad_eve_multipliers
    ):
        sim = Simulation(
            NO_GUESTS,
            NO_CONNECTIONS,
            m,
            MAX_CAPACITY,
            ATTENDANCE_SENSITIVITY,
            p,
            r,
        )

        attendance, group_happiness = zip(*[sim.step() for _ in range(NIGHTS)])
        average_attendance = sum(attendance[-SHOW_LAST:]) / SHOW_LAST
        score = (MAX_CAPACITY - average_attendance) ** 2
        if score < best_score:
            best_score = score
            params = (p, r, m)

    p, r, m = params
    print(
        f"PEER_PRESSURE = {p}, OPINION_RECOVERY = {r}, BAD_EVE_MULTIPLIER = {m}"
    )

    sim = Simulation(
        NO_GUESTS,
        NO_CONNECTIONS,
        m,
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
