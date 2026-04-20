import numpy as np
from scipy.spatial.transform import Rotation as R

from src.math.Mat4x4 import Mat4x4
from src.math.utils_matrix import is_same_matrix

# config = 'zxz' # in lover-case to use extrinsic rotations in scipy
# config = 'XYZ'
config = 'ZXZ'# in upper-case to use intrinsic rotations in scipy

phi, theta, psi = np.radians((30, 45, 60))
# rotation_matrix = Mat4x4(R.from_euler(config, (phi, theta, psi)).as_matrix())
# print(rotation_matrix)

# print()
# mat_x = Mat4x4.rotation_x(phi)
# mat_y = Mat4x4.rotation_y(theta)
# mat_z = Mat4x4.rotation_z(psi)
# # mat_xyz = mat_x * mat_y * mat_z
# mat_xyz = mat_z * mat_y *  mat_x
# print(mat_xyz)
# # print("is the same:", is_same_matrix(mat_xyz, mat))
# print("is the same:", is_same_matrix(mat_xyz, rotation_matrix))
#


mat = Mat4x4.rotation_euler(phi, theta, psi, configuration=config)
print()
print(mat)


print()
rotation_matrix_intrinsic = (R.from_euler(config, (phi, theta, psi)).as_matrix())

# Print matrix
print(rotation_matrix_intrinsic)

print("is the same:", is_same_matrix(mat, rotation_matrix_intrinsic))
