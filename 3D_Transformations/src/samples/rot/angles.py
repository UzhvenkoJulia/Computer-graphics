import numpy as np

# phi = arctan2(1, 1)
# print(np.degrees(phi))
#
# phi = arctan2(-1, 1)
# print(np.degrees(phi))
#
# phi = arctan2(-1, -1)
# print(np.degrees(phi))
#
# phi = arctan2(1, -1)
# print(np.degrees(phi))

N = 30
for i in range(N):
    alpha = 2 * np.pi * i / N
    x = np.cos(alpha)
    y = np.sin(alpha)

    phi = np.arctan2(y, x)
    psi = np.arctan(y / x)

    alpha = float(np.degrees(alpha))
    phi = float(np.degrees(phi))
    psi = float(np.degrees(psi))

    print("===============")
    print(x, y)
    print(f"{alpha=}, {phi=}, {psi=}")
