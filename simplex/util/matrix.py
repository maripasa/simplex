from fractions import Fraction
from random import randint

class Matrix:
    def __init__(self, data: list[list[float]]):
        if not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Inconsistent row lengths")

        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

    def __repr__(self):
        return f"<Matrix({self.data})>"

    def __str__(self):
        return '\n'.join(['\t'.join(map(str, row)) for row in self.data])

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Different dimensions between the Matrices")
        result = [
            [
                self.data[i][j] + self.data[i][j]
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other) -> 'Matrix':
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError(
                    "Number of columns of the first matrix must be equal to the number of rows of the second matrix")
            result = [
                [
                    sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                    for j in range(other.cols)
                ]
                for i in range(self.rows)
            ]
        elif isinstance(other, (int, float)):
            result = [
                [
                    self.data[i][j] * other
                    for j in range(self.cols)
                ]
                for i in range(self.rows)
            ]
        else:
            raise ValueError(f"Unsupported operand type(s) for *: 'Matrix' and '{other}'")
        return Matrix(result)

    def transpose(self):
        result = [
            [
                self.data[j][i]
                for j in range(self.rows)
            ]
            for i in range(self.cols)
        ]
        return Matrix(result)
    
    def inverse(self):
        
        data = [[Fraction(num) for num in row] for row in matrix.data]
                
        

def laplace_determinant(matrix):
    if matrix.rows != matrix.cols:
        raise ValueError("Matrix isn't a Square Matrix")
    if matrix.rows == 2:
        result = matrix.data[0][0] * matrix.data[1][1] - matrix.data[0][1] * matrix.data[1][0]
        return result
    else:
        result = 0
        for j in range(matrix.cols):
            cofactor = []
            for row in range(1, matrix.rows):
                cofactor_row = []
                for col in range(matrix.cols):
                    if col != j:
                        cofactor_row.append(matrix.data[row][col])
                cofactor.append(cofactor_row)
            result += ((-1) ** j) * matrix.data[0][j] * laplace_determinant(Matrix(cofactor))
        return result


def determinant(matrix):
    if matrix.rows != matrix.cols:
        raise ValueError("Determinant can only be calculated for square matrices.")

    data = [[Fraction(num) for num in row] for row in matrix.data]
    n = matrix.rows
    sign = 1

    for diag in range(n):
        if data[diag][diag] == 0:
            for k in range(diag + 1, n):
                if data[k][diag] != 0:
                    data[diag], data[k] = data[k], data[diag]
                    sign *= -1
                    break
            else:
                return 0

        for i in range(diag + 1, n):
            factor = Fraction(data[i][diag], data[diag][diag])
            for j in range(diag, n):
                data[i][j] -= factor * data[diag][j]

    det = Fraction(1)
    for i in range(n):
        det *= data[i][i]
    det *= sign
    print(sign)
    return float(det)

def random_matrix(i, j, min_value=0, max_value=9):
    result = []
    for row in range(i):
        line = []
        for col in range(j):
            line.append(randint(min_value, max_value))
        result.append(line)
    
    return Matrix(result)

def identity_matrix(n):
    result = []
    for row in range(n):
        line = []
        for col in range(n):
            if col == row:
                line.append(1)
            else:
                line.append(0)
        result.append(line)

    return Matrix(result)
        
    
matrix1 = Matrix([[1, 2, 3, 5],
                  [4, 5, 6, 7],
                  [7, 8, 9, 8],
                  [1, 6, 7, 2]])
                  
matrix2 = Matrix([[1, 5, 3, 8],
                  [2, 9, 4, 7],
                  [6, 0, 3, 1],
                  [8, 5, 7, 2]])

matrix3 = Matrix([[2, 7, 4, 1],
                  [8, 3, 6, 0],
                  [5, 9, 2, 4],
                  [8, 1, 7, 3]])

print(determinant(matrix1))
print(laplace_determinant(matrix1))

print(determinant(matrix2))
print(laplace_determinant(matrix2))

print(determinant(matrix3))
print(laplace_determinant(matrix3))

print(random_matrix(4, 4))
print(identity_matrix(4))