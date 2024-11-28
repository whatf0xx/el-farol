import matplotlib.pyplot as plt
from simulation import Simulation
import numpy as np


NIGHTS = 800
SHOW_LAST = 100
NO_GUESTS = 300
NO_CONNECTIONS = 11
MAX_CAPACITY = 60
PEER_PRESSURE = 1.2
BAD_EVENING_MULTIPLIER = 4.0
ATTENDANCE_SENSITIVITY = 0.5
OPINION_RECOVERY = 0.21


if __name__ == "__main__":
    # peer_pressures = np.linspace()
    sim = Simulation(
        NO_GUESTS,
        NO_CONNECTIONS,
        BAD_EVENING_MULTIPLIER,
        MAX_CAPACITY,
        ATTENDANCE_SENSITIVITY,
        PEER_PRESSURE,
        OPINION_RECOVERY,
    )

    attendance, group_happiness = zip(*[sim.step() for _ in range(NIGHTS)])

    plt.figure()
    plt.plot(attendance[-SHOW_LAST:])
    plt.title("Attendance")

    plt.figure()
    plt.plot(group_happiness[-SHOW_LAST:])
    plt.title("Group happiness")

    plt.show()
