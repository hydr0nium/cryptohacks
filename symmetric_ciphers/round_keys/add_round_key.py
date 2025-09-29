state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    return bytes([x for xs in matrix for x in xs])


def add_round_key(s, k):
    result_matrix = []
    for left,right in zip(s,k):
        row = []
        for a,b in zip(left,right):
            row.append(a ^ b)
        result_matrix.append(row)
    return result_matrix
        

applied_round_key = add_round_key(state, round_key)
print(matrix2bytes(applied_round_key))

