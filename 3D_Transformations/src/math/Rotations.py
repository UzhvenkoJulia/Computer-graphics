import numpy as np


def rotation_matrix_x(phi):
    """
    Builds the rotation matrix around the X axis by the given angle.

    Parameters:
    theta (float): Rotation angle in radians.

    Returns:
    numpy.ndarray: 3x3 rotation matrix.
    """
    cos_phi, sin_phi =  np.cos(phi), np.sin(phi)
    return np.array([
        [1,         0,            0, ],
        [0,    cos_phi,    -sin_phi, ],
        [0,    sin_phi,     cos_phi, ],
    ])


def rotation_matrix_y(phi):
    """
    Builds the rotation matrix around the Y axis by the given angle.

    Parameters:
    theta (float): Rotation angle in radians.

    Returns:
    numpy.ndarray: 3x3 rotation matrix.
    """
    cos_phi, sin_phi =  np.cos(phi), np.sin(phi)
    return np.array([
        [ cos_phi,     0,     sin_phi ],
        [       0,     1,           0 ],
        [-sin_phi,     0,     cos_phi ],
    ])

def rotation_matrix_z(phi):
    """
    Builds the rotation matrix around the Z axis by the given angle.

    Parameters:
    theta (float): Rotation angle in radians.

    Returns:
    numpy.ndarray: 3x3 rotation matrix.
    """
    cos_phi, sin_phi =  np.cos(phi), np.sin(phi)

    return np.array([
        [cos_phi,   -sin_phi,     0 ],
        [sin_phi,    cos_phi,     0 ],
        [      0,          0,     1 ],
    ])


def get_rotation_angle(matrix):
    # Check orthogonality of R
    if not np.allclose(np.dot(matrix.T, matrix), np.eye(2)) or not np.isclose(np.linalg.det(matrix), 1):
        raise ValueError("Matrix is not a valid rotation matrix.")

    """
    Computes the rotation angle (in radians) from a 2D rotation matrix.
    """
    if matrix.shape != (2, 2) and matrix.shape != (3, 3):
        raise ValueError("Invalid rotation matrix!")

    if matrix.shape == (3, 3):
        matrix = matrix[:2, :2]

    # Extract sin and cos values
    cos_theta = matrix[0, 0]
    sin_theta = matrix[1, 0]

    # Compute angle via arctan2
    angle = np.arctan2(sin_theta, cos_theta)
    return angle


# Usage example:
if __name__ == "__main__":
    euler_angles_45_45_30 = [45, 15, 30]
    x = np.radians(euler_angles_45_45_30[0])  # Angle in degrees is converted to radians
    y = np.radians(euler_angles_45_45_30[1])  # Angle in degrees is converted to radians
    z = np.radians(euler_angles_45_45_30[2])  # Angle in degrees is converted to radians

    Rx = rotation_matrix_x(x)
    Ry = rotation_matrix_y(y)
    Rz = rotation_matrix_z(z)

    print("\nRotation matrix for sequential Euler angles:")
    print()
    print(Rx @ Ry @ Rz)

