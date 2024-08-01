from fractions import Fraction
from random import randint
from typing import Any

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

    def transpose(self) -> 'Matrix':
        result = [
            [
                self.data[j][i]
                for j in range(self.rows)
            ]
            for i in range(self.cols)
        ]
        return Matrix(result)
    
    def inverse(self) -> 'Matrix':
        if self.cols != self.rows:
            raise ValueError("Matrix isn't square")
        if determinant(self) == 0:
            raise ValueError("Matrix determinant = 0")
            
        identity_data = identity_matrix(self.rows) 
        data = [[Fraction(num) for num in row] for row in self.data]
        identity = [[Fraction(num) for num in row] for row in identity_data.data]
        n = self.rows
        for diag in range(n):
            if data[diag][diag] == 0:
                for k in range(diag, n):
                    if data[k][diag] != 0:
                        data[diag], data[k] = data[k], data[diag]
                        identity[diag], identity[k] = identity[k], identity[diag]
                        break
                else:
                    return 0
            
            if data[diag][diag] != 1:
                factor = data[diag][diag]
                for k in range(n):
                    data[diag][k] /= factor                
                    identity[diag][k] /= factor

            for i in range(n):
                if i == diag:
                    continue
                factor = data[i][diag]
                for j in range(n):
                    data[i][j] -= factor * data[diag][j]
                    identity[i][j] -= factor * identity[diag][j]
        
        result = [[float(num) for num in row] for row in identity]
        return Matrix(result)
        

def laplace_determinant(matrix: Matrix) -> float:
    if matrix.rows != matrix.cols:
        return 0
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


def determinant(matrix: Matrix) -> float:
    if matrix.rows != matrix.cols:
        return 0

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
    return float(det)

def randint_matrix(i: int, j: int, min_value: float = 0, max_value: float = 9) -> Matrix:
    result = []
    for row in range(i):
        line = []
        for col in range(j):
            line.append(randint(min_value, max_value))
        result.append(line)
    
    return Matrix(result)

def identity_matrix(n: int) -> Matrix:
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
        
def cramer_solution(A: Matrix, b: Matrix) -> Matrix:
    if A.rows != A.cols:
        ValueError("Invalid A: Matrix isn't square")
    if determinant(A) == 0:
        ValueError("Invalid A: Matrix has many or no solutions (|A| = 0)")
    if b.rows != A.rows:
        ValueError("Invalid b: b has less items than A has rows.")
    if b.cols != 1:
        ValueError("Invalid b: b has multiple columns.")
        
    A_data = [[Fraction(num) for num in row] for row in A.data]
    b_data = [[Fraction(num) for num in row] for row in b.data]
    x = []
    A_det = determinant(A)
    for j in range(A.cols):
        aux = A_data
        for i in range(A.rows):
            aux[i][j] = b_data[i][0]
        x.append([Fraction(determinant(Matrix(aux)), A_det)])
    
    result = [[float(num) for num in row] for row in x]
    return Matrix(result)
    
A = Matrix([[2, 1, -1],
            [3, -2, 4],
            [1, 1, 1]])
b = Matrix([[3],
            [17],
            [9]])

cramer_solution(A, b)