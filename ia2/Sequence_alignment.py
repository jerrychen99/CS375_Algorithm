import sys

def read_cost_matrix(fns=''):
    """
    Reads a cost matrix file in CSV format, where:
      - The first line has the y-symbols as columns (ignoring the first column).
      - Each subsequent line starts with an x-symbol, followed by integer costs.

    Returns:
      loss_matrix (list of lists),
      x_indexdict (dict),
      y_indexdict (dict)
    """
    loss_matrix = []
    x_indexdict = {}
    y_indexdict = {}

    with open(fns, 'r') as f:
        line_idx = 0
        for line in f:
            parts = line.strip().split(',')
            if line_idx == 0:
                ys = [y.strip() for y in parts[1:]]
            else:
                x = parts[0].strip()
                x_indexdict[x] = line_idx - 1

                row_costs = []
                for j, val in enumerate(parts[1:]):
                    y_indexdict[ys[j]] = j
                    row_costs.append(int(val.strip()))
                loss_matrix.append(row_costs)

            line_idx += 1

    return loss_matrix, x_indexdict, y_indexdict


def Edit_dist(x, x_size, y, y_size, cost_matrix, x_indexdict, y_indexdict):
    D = [[0] * (y_size + 1) for _ in range(x_size + 1)]
    traceback = [[None] * (y_size + 1) for _ in range(x_size + 1)]

    for i in range(0, x_size + 1):
        if i > 0:
            D[i][0] = D[i-1][0] + cost_matrix[x_indexdict.get(x[i-1], x_indexdict['-'])][y_indexdict['-']]
            traceback[i][0] = "D" 
    for j in range(0, y_size + 1):
        if j > 0:
            D[0][j] = D[0][j-1] + cost_matrix[x_indexdict['-']][y_indexdict.get(y[j-1], y_indexdict['-'])]
            traceback[0][j] = "I" 

    for i in range(1, x_size + 1):
        for j in range(1, y_size + 1):
            if x[i - 1] == y[j - 1]:
                cost = 0
            else:
                cost = cost_matrix[x_indexdict.get(x[i-1], x_indexdict['-'])][y_indexdict.get(y[j-1], y_indexdict['-'])]

            delete = D[i-1][j] + cost_matrix[x_indexdict.get(x[i-1], x_indexdict['-'])][y_indexdict['-']] 
            insert = D[i][j-1] + cost_matrix[x_indexdict['-']][y_indexdict.get(y[j-1], y_indexdict['-'])]
            substitute = D[i-1][j-1] + cost 

            D[i][j] = min(delete, insert, substitute)

            if D[i][j] == substitute:
                traceback[i][j] = "S"  
            elif D[i][j] == delete:
                traceback[i][j] = "D" 
            else:
                traceback[i][j] = "I"

    return D, traceback


def traceback_alignment(seq1, seq2, traceback):
    aligned_seq1 = ""
    aligned_seq2 = ""

    i, j = len(seq1), len(seq2)

    while i > 0 or j > 0:
        if i > 0 and j > 0 and traceback[i][j] == "S":
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            i -= 1
            j -= 1
        elif i > 0 and traceback[i][j] == "D":
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = "-" + aligned_seq2
            i -= 1
        else:
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            j -= 1

    return aligned_seq1, aligned_seq2


def align_sequences(seq1, seq2, cost_matrix, x_indexdict, y_indexdict):
    D, traceback = Edit_dist(seq1, len(seq1), seq2, len(seq2), cost_matrix, x_indexdict, y_indexdict)
    aligned_seq1, aligned_seq2 = traceback_alignment(seq1, seq2, traceback)
    return aligned_seq1, aligned_seq2, D[len(seq1)][len(seq2)]


def process_input(input_file, cost_matrix, x_indexdict, y_indexdict, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        for line in lines:
            parts = line.strip().split(',')
            
            seq1, seq2 = parts
            aligned_seq1, aligned_seq2, cost = align_sequences(seq1, seq2, cost_matrix, x_indexdict, y_indexdict)
            f.write(f"{aligned_seq1},{aligned_seq2}:{cost}\n")


if __name__ == "__main__":
    cost_matrix, x_indexdict, y_indexdict = read_cost_matrix("imp2cost.txt")
    process_input("imp2input.txt", cost_matrix, x_indexdict, y_indexdict, "imp2output.txt")
