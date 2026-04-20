import math

import numpy as np
from scipy.spatial.transform import Rotation
from scipy.spatial.transform import Rotation as R

from src.math.Mat3x3 import Mat3x3
from src.math.Mat4x4 import Mat4x4
from src.math.Quaternion import Quaternion
from src.math.Rotations import get_rotation_angle


def is_orthogonal(matrix, tol=1e-6):
    """
    Checks whether the matrix is orthogonal (R^T * R = I).
    """
    matrix = Mat4x4(matrix)
    identity = Mat4x4()

    mul_mat = matrix.T * matrix
    return np.allclose(mul_mat.data, identity.data, atol=tol)

def is_same_matrix(matrix1, matrix2, tol=1e-6):
    """
    Checks whether two matrices are equal.
    """
    matrix1 = Mat4x4(matrix1)
    matrix2 = Mat4x4(matrix2)
    mat_dif = matrix1 - matrix2

    return mat_dif.norm() < tol

# def decompose_affine(transition):
#
#     if not isinstance(transition, (np.ndarray, Mat4x4)):
#         raise TypeError("Transformation error.")
#
#     if isinstance(transition, Mat4x4):
#         transition = transition.data
#
#     if transition.shape != (4, 4):
#         raise ValueError("Matrix must be 4x4.")
#
#     # Extract translation
#     translation = transition[:3, 3]
#
#     # Extract RS matrix
#     rs = transition[:3, :3]
#
#     # Compute scale
#     scale_x = np.linalg.norm(rs[:, 0])
#     scale_y = np.linalg.norm(rs[:, 1])
#     scale_z = np.linalg.norm(rs[:, 2])
#     scales = np.array([scale_x, scale_y, scale_z])
#
#     # Compute rotation
#     rotation = rs / scales
#
#     # # angle = get_rotation_angle(rotation)
#     #
#     # return translation, rotation, scales
#
#
#     # Polar decomposition to correct possible distortions
#     U, _, Vt = np.linalg.svd(rotation)
#     R = U @ Vt  # Pure orthogonal rotation matrix
#
#     # Get rotation axis and angle
#     rot = Rotation.from_matrix(R)
#     axis, angle = rot.as_rotvec(), np.degrees(rot.magnitude())
#
#     return T, scale_x, R, axis, angle


def decompose_translation_quaternion_scale(T):
    """
    Decomposition of a 4x4 transformation matrix into components:
    - Translation
    - Scale
    - Rotation (as quaternion)

    Input: 4x4 matrix T
    Output: translation, scale, quaternion
    """

    # 1. Extract Translation
    translation = T[:3, 3]

    # 2. Extract rotation and scale
    M = T[:3, :3]  # Upper-left 3x3 sub-matrix (contains scale and rotation)

    # 3. Compute Scale
    scale = np.linalg.norm(M, axis=0)  # Length of each column

    # 4. Obtain rotation matrix (normalize)
    R_matrix = M / scale  # Remove scale influence

    # 5. Convert rotation matrix to quaternion
    quaternion = R.from_matrix(R_matrix).as_quat()  # Output: [x, y, z, w]

    quaternion = Quaternion(quaternion[3], *quaternion[:3])

    return translation, quaternion, scale


def decompose_affine(matrix):
    """
    Decomposition of a 4x4 matrix into translation (T), scale (S) and rotation (R).
    """
    # Extract translation (last column without last element)
    T = matrix[:3, 3]

    # Extract linear transformation (upper-left 3x3 sub-matrix)
    M = matrix[:3, :3]

    # Get scale (column lengths)
    S = np.linalg.norm(M, axis=0)

    # Normalize M to remove scale and obtain pure rotation
    R = M / S  # Divide each column by the corresponding scale value

    # Polar decomposition to correct possible distortions
    U, _, Vt = np.linalg.svd(R)
    R = U @ Vt  # Pure orthogonal rotation matrix

    # Get rotation axis and angle
    rot = Rotation.from_matrix(R)
    # axis, angle = rot.as_rotvec(), np.degrees(rot.magnitude())
    axis, angle = rot.as_rotvec(), rot.magnitude()

    return T, R, S, axis, angle

def decompose_affine3(transition):

        if not isinstance(transition, (np.ndarray, Mat3x3)):
            raise TypeError("Transformation error.")

        if isinstance(transition, Mat3x3):
            transition = transition.data

        if transition.shape != (3, 3):
            raise ValueError("Matrix must be 3x3.")

        # Extract translation
        translation = transition[:2, 2]

        # Extract RS matrix
        rs = transition[:2, :2]

        # Compute scale
        scale_x = np.linalg.norm(rs[:, 0])
        scale_y = np.linalg.norm(rs[:, 1])
        scales = np.array([scale_x, scale_y])

        # Compute rotation
        rotation = rs / scales

        angle = get_rotation_angle(rotation)

        return translation, angle, scales

def decompose_affine_2(matrix):
    """
    Decomposition of a 4x4 matrix into translation (T), scale (S) and rotation (R).
    Also computes rotation axis and angle.
    """
    # Extract translation (last column without last element)
    T = matrix[:3, 3]

    # Extract linear transformation (upper-left 3x3 sub-matrix)
    M = matrix[:3, :3]

    # Get scale (column lengths)
    S = np.linalg.norm(M, axis=0)

    # Normalize M to remove scale and obtain pure rotation
    # Guard against division by zero if scale is 0
    R = M / S

    # --- Get rotation angle ---
    # cos(theta) = (Tr(R) - 1) / 2
    trace = R[0, 0] + R[1, 1] + R[2, 2]
    cos_theta = np.clip((trace - 1.0) / 2.0, -1.0, 1.0)
    angle = np.arccos(cos_theta)

    # --- Get rotation axis ---
    if np.isclose(angle, 0.0):
        # Case 0: No rotation, axis can be arbitrary
        axis = np.array([1.0, 0.0, 0.0])

    elif np.isclose(angle, np.pi):
        # Case 180 degrees: sin(theta) = 0, the r_ij difference method does not work.
        # Find axis via diagonal elements.
        diag = np.diag(R)
        axis = np.sqrt(np.maximum((diag + 1.0) / 2.0, 0.0))

        # Determine signs of axis components from off-diagonal elements
        if R[0, 1] < 0: axis[1] = -axis[1]
        if R[0, 2] < 0: axis[2] = -axis[2]
        if R[1, 2] < 0 and axis[1] * axis[2] > 0: axis[2] = -axis[2]

        axis = axis / np.linalg.norm(axis)

    else:
        # General case: use antisymmetric part of the matrix
        # u = [r21 - r12, r02 - r20, r10 - r01]
        axis = np.array([
            R[2, 1] - R[1, 2],
            R[0, 2] - R[2, 0],
            R[1, 0] - R[0, 1]
        ])
        # Normalize to get a unit vector
        axis = axis / np.linalg.norm(axis)

    return T, R, S, axis, angle

if __name__ == '__main__':
    an, ax = math.pi / 7, (1, 2, 1)
    R = Mat4x4.rotation(an, ax)
    T  = Mat4x4.translation(1, 1, 1)
    S = Mat4x4.scale(2, 2, 2)

    T1, R1, S1, axis1, angle1 = decompose_affine_2(R)
    T2, R2, S2, axis2, angle2 = decompose_affine_2(T * R * S)
    print(an, ax)
    print(angle1, axis1)
