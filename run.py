import matplotlib.pyplot as plt
from simulation import Simulation


NIGHTS = 800
SHOW_LAST = 100
NO_GUESTS = 300
NO_CONNECTIONS = 3
MAX_CAPACITY = 60
PEER_PRESSURE = 0.9
BAD_EVENING_MULTIPLIER = 2.0
ATTENDANCE_SENSITIVITY = 0.5
OPINION_RECOVERY = 0.21


if __name__ == "__main__":
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
