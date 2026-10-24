EMPTY = " "


class Board:
    """A square Tic-Tac-Toe board."""

    def __init__(self, size=3):
        if size < 3:
            raise ValueError("size must be at least 3")
        self._size = size
        self._grid = [[EMPTY] * size for _ in range(size)]

    @property
    def size(self):
        return self._size

    def cell(self, row, col):
        """Return the mark at row, col (counting from 0)."""
        return self._grid[row][col]

    def _in_range(self, row, col):
        return 0 <= row < self._size and 0 <= col < self._size

    def place_mark(self, row, col, mark):
        """Place mark at row, col. Return True if placed, False if not allowed."""
        if not self._in_range(row, col):
            return False
        if self._grid[row][col] != EMPTY:
            return False
        self._grid[row][col] = mark
        return True
    
    def remove_mark(self, row, col):
        """Remove mark at row,col. Return Nothing"""
        if self._in_range(row,col):
            self._grid[row][col] = EMPTY 

    def empty_cells(self):
        """Return a list of (row, col) pairs for every empty cell."""
        return [(r, c) for r in range(self._size) for c in range(self._size)
                if self._grid[r][c] == EMPTY]

    def is_full(self):
        return not self.empty_cells()

    def copy(self):
        """Return an independent copy of this board."""
        clone = Board(self._size)
        clone._grid = [row[:] for row in self._grid]
        return clone

    def has_won(self, mark):
        """Return True if mark fills a whole row, column, or diagonal."""
        for row in self._grid:
            if all(cell == mark for cell in row):
                return True
        for col in range(self._size):
            if all(self._grid[row][col] == mark for row in range(self._size)):
                return True
        if all(self._grid[i][i] == mark for i in range(self._size)):
            return True
        return all(self._grid[i][self._size - 1 - i] == mark for i in range(self._size))


    def __str__(self):
        separator = "-+-".join("-" * self._size)
        lines = []
        for i, row in enumerate(self._grid):
            lines.append(" | ".join(row))
            if i < self._size - 1:
                lines.append(separator)
        return "\n".join(lines)