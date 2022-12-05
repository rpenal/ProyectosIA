import os
import webview
#from menu import ventana_metodos_logicos
import time
tiempo_inicio = time.time()
def find_options(length, filled, pattern='', empty=''):
    """ This function finds all possibilities for the starting condition of the rows or columns. """

    total_empty = length - sum(filled)
    extra = total_empty - len(filled) + 1
    lines = []

    for pad in range(0, extra + 1):
        # Loop over each possible set of padding.

        line = ''
        blanks = len(filled)
        total_blanks = total_empty - pad

        # Set the first value of the sub-string.
        line += '0' * pad
        line += '1' * filled[0]

        # Subtract from the number of dividers left.
        blanks -= 1

        if blanks > 0:
            # If there are still dividers, leave a blank for it.
            line += '0'

            # Subtract this divider from the total blanks left.
            total_blanks -= 1

        if len(filled) > 1:
            # If the string has not been fully built yet, then generate the next sub-string.
            subs = find_options(length - len(line), filled[1:])

            # Append this section with the sub-sections found in the recursion.
            lines.extend([line + sub for sub in subs])
        else:
            # There are no parts left so pad with the remaining blanks.
            line += '0' * total_blanks

            # Add the string to the possible values.
            lines.append(line)

    if len(lines[0]) == length and pattern != '':
        # Generate a bitmask from the pattern.
        mask = int(pattern, base=2)

        # A filled out pattern was passed in, check to see if the current possibility is valid.
        lines = [line for line in lines if (int(line, base=2) & mask) == mask]

    if len(lines[0]) == length and empty != '':
        # Generate a bitmask from the empty positions.
        mask = int(empty, base=2)

        # An empty position pattern was passed in, check to see if the current possibility is valid.
        lines = [line for line in lines if not int(line, base=2) & mask]

    # Return the possible values.
    return lines

def find_overlap(length, patterns):
    """ This function finds the overlap between the current possibilities for a row or column. """

    # Set the initial masks to everything set.  This handles up to a 32x32 grid.
    overlap = 0xFFFFFFFF

    for pattern in patterns:
        # Convert each possibility to an integer based on the string bit pattern and generate
        # the overlap mask.
        overlap &= int(pattern, base=2)

    # Return the value as a bit pattern string.
    return '{0:b}'.format(overlap).zfill(length)

def update_existing(col_existing, row_existing):
    """
        This function updates the rows based on the columns and vice-versa.  It basically rotates
        one matrix in memory and compares it to the other one.
    """

    for row_index, _ in enumerate(col_existing):
        for col_index, _ in enumerate(row_existing):
            if col_existing[row_index][col_index] == '1':
                row_existing[col_index] \
                    = row_existing[col_index][:row_index] \
                    + '1' \
                    + row_existing[col_index][row_index+1:]

            if row_existing[row_index][col_index] == '1':
                col_existing[col_index] \
                    = col_existing[col_index][:row_index] \
                    + '1' \
                    + col_existing[col_index][row_index+1:]

    return row_existing, col_existing

def solve(length, horizontal_grid, vertical_grid, max_passes=0):
    
    """
        This function will solve a nonogram given the length, horizontal_grid, and vertical_grid.

        Currently, passing in a partially solved puzzle is not supported.  The way nonograms are
        setup, it should never be required to have a partially solved puzzle to beging with unlike,
        for instance, sudokus.

        Even if previous steps have been processed, if max_passes has been passed, the solver
        starts from the beginning again.  This is because the user may have edited the puzzle
        row and column numbers which would change the solution.  Even 25x25 puzzles are solved in
        under a second, so this should not be an issue from a user-perspective.
    """

    # Initialize the existing tables.
    horizontal_existing = []
    vertical_existing = []

    # Initialize the backup tables.  These are used to compare with the current values in order to
    # see if the script has finished.  This is done instead of checking that every row and column
    # is correct because, if there is a bug or data entry issue, this could cause and endless loop.
    horizontal_backup = []
    vertical_backup = []

    # Initialize the empty tables.
    horizontal_empty = []
    vertical_empty = []

    for row in horizontal_grid:
        # Find the initial patterns for each row.
        patterns = find_options(length, row)

        # Find the initial filled out and empty values for each row.
        horizontal_existing.append(find_overlap(length, patterns))
        horizontal_empty.append(find_empty(length, patterns))

    for col in vertical_grid:
        # Find the initial patterns for each column.
        patterns = find_options(length, col)

        # Find the initial filled out and empty values for each column.
        vertical_existing.append(find_overlap(length, patterns))
        vertical_empty.append(find_empty(length, patterns))

    # Initialize the done flag as well as the number of passes needed to solve the puzzle.
    passes = 0
    done = 0

    while not done:
        # If changes were made to the grid, keep trying to solve the puzzle.

        # Set the backed-up data to the current data.
        horizontal_backup = horizontal_existing[:]
        vertical_backup = vertical_existing[:]

        # Update the existing tables based on their counterpart table.
        vertical_existing, horizontal_existing \
            = update_existing(horizontal_existing, vertical_existing)

        # Update the empty tables based on their counterpart table.
        vertical_empty, horizontal_empty \
            = update_existing(horizontal_empty, vertical_empty)

        for index, _ in enumerate(horizontal_grid):
            # Find the current patterns for each row.
            patterns = find_options(
                length,
                horizontal_grid[index],
                horizontal_existing[index],
                horizontal_empty[index]
            )

            # Update the horizontal positions.
            horizontal_existing[index] = find_overlap(length, patterns)

            # Find the empty positions for the available patterns.
            horizontal_empty[index] = find_empty(length, patterns)

        for index, _ in enumerate(vertical_grid):
            # Find the current patterns for each column.
            patterns = find_options(
                length,
                vertical_grid[index],
                vertical_existing[index],
                vertical_empty[index]
            )

            # Update the vertical positions.
            vertical_existing[index] = find_overlap(length, patterns)

            # Find the empty positions for the available patterns.
            vertical_empty[index] = find_empty(length, patterns)

        if (horizontal_existing == horizontal_backup and vertical_existing == vertical_backup):
            # Nothing changed on this last pass.  Set the flag to done so we do not end up in
            # an infinite loop.
            done = 1

        passes += 1

        if passes == int(max_passes):
            # This allows for iterating through the solution one step at a time.
            # It was a feature request from a YouTube user.
            done = 1
    
    
    return horizontal_existing, horizontal_empty, passes

def find_empty(length, potential):
    """ This function finds the empty positions based of the potential fill positions. """

    # Make a copy of the potential patterns.
    patterns = potential[:]

    for index, pattern in enumerate(patterns):
        # Flip the bits of each position.
        patterns[index] = ''.join('1' if bit == '0' else '0' for bit in pattern)

    # Find the overlap of the empty positions.
    empty = find_overlap(length, patterns)

    return empty



def main():
    """ This is the main function of the program. """
    
    window = webview.create_window("Nonogram Solver", "web/main.html")
    window.expose(solve)

    os_type = os.name

    if os_type == "posix":
        # POSIX works properly with the default rendering engine.
        webview.start(http_server=True)
    elif os_type == "nt":
        # Edge does not currently work properly with local files so fallback on CEF.
        webview.start(gui="cef", http_server=True)
    else:
        # Unknown system.  Assume that it works properly with the default rendering engine.
        webview.start(http_server=True)
    
    
tiempo_final = time.time()
print(tiempo_final-tiempo_final)
if __name__ == '__main__':
   # ventana_metodos_logicos.destroy()
    
    
    
    main()
