import numpy as np

def scale_matrix(s_x=1, s_y=1, s_z=1):
    return np.array([
        [ s_x,   0,      0 ],
        [ 0,    s_y,     0 ],
        [ 0,      0,   s_z ]
    ])


