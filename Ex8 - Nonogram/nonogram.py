# FILE : nonogram.py
# WRITER : Ron Shuvy , ronshuvy , 206330193
# EXERCISE : intro2cs1 2019 ex8


def get_row_variations(row, blocks):
    """
    Returns a list of all possibilities to color a given row by following
    the constraints
    :param row: a list represents row in board with values : -1, 0, 1
    :param blocks: list of constraints
    :return: lists of list with values 0 or 1
    """
    if not row:
        return []

    if not blocks:  # if block is empty - all variations is wanted
        blocks = [-1]

    # Checks if the row meets the prerequisites :
    # having enough cells in total and enough available cells to color
    colored_cell_needed = sum(blocks)  # how much available cells do we need
    if len(row) < colored_cell_needed + len(blocks)-1\
            or len(row) - row.count(0) < colored_cell_needed:
        return []

    # Prerequisites are met, let's go
    return _get_row_var_helper(row, blocks, 0, 0, 0)


def _get_row_var_helper(row, blocks, row_ind, blk_ind, seq):
    """
    Returns a list of all possibilities to color a given row by following
    the constraints
    :param row: a list represents row in board with values : -1, 0, 1
    :param blocks: list of constraints
    :param row_ind: an index in row list - which cell to check each time
    :param blk_ind: an index in blocks list - which sequence to complete in
    present
    :param seq: counter of consecutively colored cells (1's)
    :return: lists of list with values 0 or 1
    """

    # We will add all valid lists into here.
    solutions = []

    for i in range(row_ind, len(row)):

        # We found free cell - let's test both options - uncolored or colored
        if row[i] == -1:
            row[i] = 0  # cell is now empty
            solutions += _get_row_var_helper(row[:], blocks, i, blk_ind, seq)
            row[i] = 1  # cell is now black
            solutions += _get_row_var_helper(row[:], blocks, i, blk_ind, seq)
            row[i] = -1  # preserves the original input
            return solutions

        if seq < blocks[blk_ind] and row[i] == 1:
            seq += 1  # another colored cell was found :)

        # uncolored cell (0) has stopped the sequence :(
        elif 0 < seq < blocks[blk_ind] and row[i] == 0:
            return []

        # We reached the desired sequence in the current constraint
        elif seq == blocks[blk_ind]:
            if row[i] == 1:  # we colored too much, the sequence is too long
                return []
            if blk_ind != len(blocks) - 1:  # more sequences to complete
                blk_ind += 1  # move on to the next constraint
                seq = 0  # resets the counter

    # Checks if all constraints are met
    if blk_ind == len(blocks) - 1 and seq >= blocks[blk_ind]:
        solutions.append(row)  # We found valid solution!

    return solutions


def get_intersection_row(rows):
    """
    Returns an intersection row between all given rows, by these instructions:
    if the cell was colored in every row - color it in the new one (val = 1)
    if it was uncolored in every row - don't color it in the new one (val = 0)
    otherwise makes it neutral in the row (val = -1)
    :param rows: list of rows (2D list)
    :return: the intersection row (list)
    """
    if not rows:
        return []  # rows is empty

    inter_row = []  # the new row

    for i, value in enumerate(rows[0]):
        inter_row.append(-1)
        if value != -1:
            val_is_common = True
            for j in range(1, len(rows)):
                if value != rows[j][i]:
                    val_is_common = False  # this value is not in every row
                    break  # move on to the next cell
            if val_is_common:
                inter_row[i] = value

    return inter_row


def conclude_from_constraints(board, constraints):
    """
    Checks which cells must be colored or not, and modifies the board
    accordingly
    :param board: game board (nested list)
    :param constraints: constraints list for rows and columns (list, list)
    :return: None
    """
    if not board or not constraints[0] or not constraints[1]:
        return  # board \ constraints is empty

    new_conclusions = True
    while new_conclusions:  # keeps iterates as long as the board modifies
        # conclude for rows
        _conclude_from_rows_constraints(board, constraints[0])

        # transposed board - now columns is the rows
        t_board = [[board[j][i] for j in range(len(board))] for i in range(
            len(board[0]))]

        # conclude for columns
        new_conclusions = \
            _conclude_from_rows_constraints(t_board, constraints[1])

        # assigns new conclusions back to the original board
        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j] = t_board[j][i]


def _conclude_from_rows_constraints(rows, constraints):
    """
    Checks which cells must be colored or not, and modifies the rows
    accordingly
    :param rows: list of rows
    :param constraints: list of constraints
    :return: True if changes were applied
    """

    changes_applied = False
    for i, row in enumerate(rows):
        if -1 in row:  # row in not completed yet
            row_variations = get_row_variations(row, constraints[i])
            if row_variations:  # list is not empty
                new_row = get_intersection_row(row_variations)
                if row != new_row:
                    rows[i] = new_row
                    changes_applied = True

    return changes_applied


def solve_easy_nonogram(constraints):
    """
    Solves an easy nonogram boards
    :param constraints: list of row and column constraints
    :return: the solved board
    """
    board_game = create_board(constraints)
    conclude_from_constraints(board_game, constraints)
    return board_game


def solve_nonogram(constraints):
    """
    Solves any nonogram board and returns list of possible solutions
    :param constraints: nested list of row and column constraints
    :return: nested list of solved boards
    """
    board = solve_easy_nonogram(constraints)
    return _solve_nonogram_helper(board, constraints, 0)


def _solve_nonogram_helper(board_game, constraints, row_ind):
    """
    Solves any nonogram board and returns list of possible solutions
    :param board_game: nested list
    :param constraints: nested list of row and column constraints
    :return: nested list of solved boards
    """
    board = copy_board(board_game)

    # conclude from current board
    conclude_from_constraints(board, constraints)

    # index of the next empty cell (value is -1)
    row_ind, col_ind = search_for_empty_cells(board, row_ind)

    if row_ind == -1:  # board is complete - no empty cell exists
        return [board]  # adding board to the solutions list

    solutions = []  # We will add all completed boards into here

    # Starts backtracking
    next_row = row_ind
    if col_ind == len(board[0]) - 1:  # last column, move to next row
        next_row += 1

    board[row_ind][col_ind] = 0
    solutions += _solve_nonogram_helper(board, constraints, next_row)

    board[row_ind][col_ind] = 1
    solutions += _solve_nonogram_helper(board, constraints, next_row)

    return solutions


def search_for_empty_cells(board, row_ind):
    """
    Searches for empty cell (value is -1) and return its index
    :param board: nested list
    :param row_ind: start searching from this index
    :return: row index and column index of the first empty cell
    if all cells are filled - returns (-1, -1)
    """
    for i in range(row_ind, len(board)):
        for j, value in enumerate(board[i]):
            if value == -1:
                return i, j
    # all cells are filled
    return -1, -1


def create_board(constraints):
    """
    Creates board game according to constraints sizes
    :param constraints: constraints for rows and columns
    :return: board (nested list)
    """
    return [[-1] * len(constraints[1]) for i in range(len(constraints[0]))]


def copy_board(board):
    """
    Clones a given board
    :param board: nested list
    :return: deep copy of board
    """
    return [row[:] for row in board]
