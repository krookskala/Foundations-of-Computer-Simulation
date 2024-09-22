import numpy as np
import matplotlib.pyplot as plt

def gaussian_elimination(coeff_matrix, result_vector):
    num_rows = len(coeff_matrix)
    for current_row in range(num_rows):
        max_row_index = np.argmax(np.abs(coeff_matrix[current_row:, current_row])) + current_row
        coeff_matrix[[current_row, max_row_index]] = coeff_matrix[[max_row_index, current_row]]
        result_vector[current_row], result_vector[max_row_index] = result_vector[max_row_index], result_vector[current_row]
        if abs(coeff_matrix[current_row, current_row]) <= 1e-10:
            raise RuntimeError("Matrix Is Degenerate Or Close To Degenerate.")
        for row in range(current_row + 1, num_rows):
            factor = coeff_matrix[row, current_row] / coeff_matrix[current_row, current_row]
            result_vector[row] -= factor * result_vector[current_row]
            coeff_matrix[row, current_row:] -= factor * coeff_matrix[current_row, current_row:]
    solutions = np.zeros(num_rows)
    for row in range(num_rows - 1, -1, -1):
        solutions[row] = (result_vector[row] - np.sum(coeff_matrix[row, row + 1:] * solutions[row + 1:])) / coeff_matrix[row, row]
    return solutions

class BoundaryConditionMatrix:
    def __init__(self, grid_size, top_value, left_value, bottom_value, right_value):
        self.coeff_matrix = np.zeros((grid_size * grid_size, grid_size * grid_size))
        self.result_vector = np.zeros(grid_size * grid_size)
        self.grid_size = grid_size
        self.top_value = top_value
        self.left_value = left_value
        self.bottom_value = bottom_value
        self.right_value = right_value
        self.initialize_coefficients()

    def initialize_coefficients(self):
        index = 0
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.handle_top_boundary(row, col, index)
                self.handle_bottom_boundary(row, col, index)
                self.handle_right_boundary(row, col, index)
                self.handle_left_boundary(row, col, index)
                self.coeff_matrix[index, index] = -4
                index += 1

    def handle_top_boundary(self, row, col, index):
        if row == self.grid_size - 1:
            self.result_vector[index] += self.top_value
        else:
            self.coeff_matrix[index, (row + 1) * self.grid_size + col] = 1

    def handle_bottom_boundary(self, row, col, index):
        if row == 0:
            self.result_vector[index] += self.bottom_value
        else:
            self.coeff_matrix[index, (row - 1) * self.grid_size + col] = 1

    def handle_left_boundary(self, row, col, index):
        if col == self.grid_size - 1:
            self.result_vector[index] += self.left_value
        else:
            self.coeff_matrix[index, row * self.grid_size + col + 1] = 1

    def handle_right_boundary(self, row, col, index):
        if col == 0:
            self.result_vector[index] += self.right_value
        else:
            self.coeff_matrix[index, row * self.grid_size + col - 1] = 1

    def get_coeff_matrix(self):
        return self.coeff_matrix

    def get_result_vector(self):
        return self.result_vector

def main():
    try:
        boundary_conditions = BoundaryConditionMatrix(40, 200, 100, 150, 50)
        solutions = gaussian_elimination(boundary_conditions.get_coeff_matrix(), boundary_conditions.get_result_vector())
        solution_grid = solutions.reshape(boundary_conditions.grid_size, boundary_conditions.grid_size)
        for row in range(39, -1, -1):
            for col in range(39, -1, -1):
                print(f"{solution_grid[row, col]:.2f}", end=" ")
            print()
        plt.imshow(solution_grid, cmap='inferno', origin='lower')
        plt.colorbar(label='Values')
        plt.title('Heatmap')
        plt.xlabel('X Axis')
        plt.ylabel('Y Axis')
        plt.show()
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()