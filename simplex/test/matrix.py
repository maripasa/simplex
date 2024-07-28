from simplex.util.matrix import *

matrix1 = Matrix([[1, 2], [3, 4]])
matrix2 = Matrix([[5, 6], [7, 8]])
matrix3 = Matrix([[1, 2, 3, 5], [4, 5, 6, 7], [7, 8, 9, 8], [1, 6, 7, 2]])
vector1 = Matrix([[1], [2], [3]])

print("Matrix 1:")
print(matrix1)

print("Matrix 2:")
print(matrix2)

print("Matrix 1 + Matrix 2:")
print(matrix1 + matrix2)

print("Matrix 1 * Matrix 2:")
print(matrix1 * matrix2)

print("Matrix 1 * 2.5:")
print(matrix1 * 2.5)

print("Transpose of Matrix 1:")
print(matrix1.transpose())

print("Vector1")
print(vector1)

try:
    print("Vector1 * Matrix3")
    print(vector1 * matrix3)
except Exception as e:
    print(e)
    print("Vector1 * Matrix3 didn't work")

try:
    print("Matrix3 * Vector1")
    print(matrix3 * vector1)
except Exception as e:
    print(e)
    print("Matrix3 * Vector1 didn't work")

print("Transpose of Vector1")
print(vector1.transpose())

print(two_by_two_determinant(matrix1))