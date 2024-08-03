from fractions import Fraction
from random import randint
from typing import Union


class Matrix:
    def __init__(self, pre_data: list[list[Union[Fraction, float, int]]]):
        if not all(len(row) == len(pre_data[0]) for row in pre_data):
            raise ValueError("Inconsistent row lengths")

        self.data = []

        for i in pre_data:
            row = []
            for item in i:
                if isinstance(item, Fraction):
                    row.append(item)
                if isinstance(item, (float, int)):
                    row.append(Fraction.from_float(item).limit_denominator(1_000_000_000_000))
            self.data.append(row)

        self.rows = len(pre_data)
        self.cols = len(pre_data[0]) if pre_data else 0

    def __repr__(self):
        return f"<Matrix({self.data})>"

    def __str__(self):
        return '\n'.join(['\t'.join(map(str, row)) for row in self.data])

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Different dimensions between the Matrices")
        result = [
            [
                self.data[i][j] + other.data[i][j]
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

        data = [[item for item in row] for row in self.data]
        identity = identity_matrix(self.rows).data

        n = self.rows
        for diag in range(n):
            if data[diag][diag] == 0:
                for k in range(diag, n):
                    if data[k][diag] != 0:
                        data[diag], data[k] = data[k], data[diag]
                        identity[diag], identity[k] = identity[k], identity[diag]
                        break

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

        return Matrix(identity)


def laplace_determinant(matrix: Matrix) -> Fraction:
    if matrix.rows != matrix.cols:
        return Fraction(0)
    if matrix.rows == 2:
        result = matrix.data[0][0] * matrix.data[1][1] - matrix.data[0][1] * matrix.data[1][0]
        return result
    else:
        result = Fraction(0)
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


def determinant(matrix: Matrix) -> Fraction:
    if matrix.rows != matrix.cols:
        return Fraction(0)

    data = [[item for item in row] for row in matrix.data]
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
                return Fraction(0)

        for i in range(diag + 1, n):
            factor = data[i][diag] / data[diag][diag]
            for j in range(diag, n):
                data[i][j] -= factor * data[diag][j]

    det = Fraction(1)
    for i in range(n):
        det *= data[i][i]
    det *= sign
    return det


def randint_matrix(i: int, j: int, min_value: int = 0, max_value: int = 9) -> Matrix:
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


def cramer_solution(a: Matrix, b: Matrix) -> Matrix:
    if a.rows != a.cols:
        ValueError("Invalid A: Matrix isn't square")
    if determinant(a) == 0:
        ValueError("Invalid A: Matrix has many or no solutions (|A| = 0)")
    if b.rows != a.rows:
        ValueError("Invalid b: b has less items than A has rows.")
    if b.cols != 1:
        ValueError("Invalid b: b has multiple columns.")

    a_data = [[item for item in row] for row in a.data]
    b_data = [[item for item in row] for row in b.data]
    x = []
    a_det = determinant(a)
    for j in range(a.cols):
        aux = a_data
        for i in range(a.rows):
            aux[i][j] = b_data[i][0]
        x.append([Fraction(determinant(Matrix(aux)), a_det)])

    return Matrix(x)
