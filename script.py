import copy

class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        self.size = 9

    def is_valid(self, num, row, col):
        if num in self.grid[row]:
            return False

        if num in [self.grid[r][col] for r in range(self.size)]:
            return False

        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_start_row, box_start_row + 3):
            for c in range(box_start_col, box_start_col + 3):
                if self.grid[r][c] == num:
                    return False

        return True

    def find_empty_cell(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return row, col
        return None

    def get_candidates(self, row, col):
        row_values = set(self.grid[row])
        col_values = {self.grid[r][col] for r in range(self.size)}
        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)

        box_values = {
            self.grid[r][c]
            for r in range(box_start_row, box_start_row + 3)
            for c in range(box_start_col, box_start_col + 3)
        }

        return set(range(1, 10)) - row_values - col_values - box_values

    def constraint_propagation(self):
        progress = True
        while progress:
            progress = False
            for row in range(self.size):
                for col in range(self.size):
                    if self.grid[row][col] == 0:
                        candidates = self.get_candidates(row, col)

                        if len(candidates) == 1:
                            num = candidates.pop()
                            self.grid[row][col] = num
                            progress = True

                        if not candidates:
                            return False

        return True

    def backtrack_solve(self):
        empty_cell = self.find_empty_cell()

        if not empty_cell:
            return True

        row, col = empty_cell
        candidates = self.get_candidates(row, col)

        for num in sorted(candidates, key=lambda x: self.constraint_count(row, col, x)):
            if self.is_valid(num, row, col):
                self.grid[row][col] = num

                if self.backtrack_solve():
                    return True

                self.grid[row][col] = 0

        return False

    def constraint_count(self, row, col, num):
        count = 0

        for r in range(self.size):
            if self.grid[r][col] == 0 and self.is_valid(num, r, col):
                count += 1

        for c in range(self.size):
            if self.grid[row][c] == 0 and self.is_valid(num, row, c):
                count += 1

        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_start_row, box_start_row + 3):
            for c in range(box_start_col, box_start_col + 3):
                if self.grid[r][c] == 0 and self.is_valid(num, r, c):
                    count += 1

        return count

    def advanced_solve(self):
        if not self.constraint_propagation():
            return False

        if self.backtrack_solve():
            return True

        return False

    def print_grid(self):
        print("+-------+-------+-------+")
        for i, row in enumerate(self.grid):
            row_str = " ".join(str(num) if num != 0 else '.' for num in row)
            print("| " + row_str[:3] + " | " + row_str[3:6] + " | " + row_str[6:] + " |")
            if (i + 1) % 3 == 0:
                print("+-------+-------+-------+")


grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solver = SudokuSolver(grid)

print("\nSudoku Puzzle to Solve:")
solver.print_grid()

if solver.advanced_solve():
    print("\nSudoku Solved:")
    solver.print_grid()
else:
    print("\nNo solution exists.")
