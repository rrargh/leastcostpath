import re


def get_hex(row, col):
    return int(hex_grid[row][col], base=16)


# http://stackoverflow.com/questions/4997851/python-dijkstra-algorithm
def dijkstra(path_plot, start, end):
    # sanity check
    if start == end:
        return "The start and terminal nodes are the same. \
        Minimum distance is 0."
    if not path_plot.has_key(start):
        return "There is no start node called " + str(start) + "."
    if not path_plot.has_key(end):
        return "There is no terminal node called " + str(end) + "."
    # create a labels dictionary
    labels = {}
    # record whether a label was updated
    order = {}
    # populate an initial labels dictionary
    for i in path_plot.keys():
        if i == start:
            # shortest distance from start to start is 0
            labels[i] = 0
        else:
            # initial labels are infinity
            labels[i] = float("inf")
    from copy import copy
    drop1 = copy(labels)  # used for looping
    # begin algorithm
    while len(drop1) > 0:
        # find the key with the lowest label
        # minNode is the node with the smallest label
        minNode = min(drop1, key=drop1.get)
        # update labels for nodes that are connected to minNode
        for i in path_plot[minNode]:
            if labels[i] > (labels[minNode] + path_plot[minNode][i]):
                labels[i] = labels[minNode] + path_plot[minNode][i]
                drop1[i] = labels[minNode] + path_plot[minNode][i]
                order[i] = minNode
        # once a node has been visited, it's excluded from drop1
        del drop1[minNode]
    # end algorithm
    # print shortest path
    temp = copy(end)
    rpath = []
    path = []
    while 1:
        rpath.append(temp)
        if order.has_key(temp):
            temp = order[temp]
        else:
            return "There is no path from %s to %s." % (
                str(start),
                str(end)
            )
        if temp == start:
            rpath.append(temp)
            break
    for j in range(len(rpath)-1, -1, -1):
        path.append(rpath[j])

    # get path directions based on vertex names
    directions = []
    for x in range(1, len(path)):
        prev_path = path[x-1]
        # get indices from path name
        prev_row_index = int(re.search("(?<=R)\d+", prev_path).group(0))
        prev_col_index = int(re.search("(?<=C)\d+", prev_path).group(0))
        next_path = path[x]
        # get indices from path name
        next_row_index = int(re.search("(?<=R)\d+", next_path).group(0))
        next_col_index = int(re.search("(?<=C)\d+", next_path).group(0))
        # compare indices
        if prev_row_index + 1 == next_row_index \
                and prev_col_index == next_col_index:
            directions.append("down")
        elif prev_row_index == next_row_index \
                and prev_col_index + 1 == next_col_index:
            directions.append("right")
    return "The shortest path from %s to %s is %s. Minimum distance is %s." % (
        start, end, str(directions), str(labels[end])
        )

hex_grid = [
    ['46B', 'E59', 'EA', 'C1F', '45E', '63'],
    ['899', 'FFF', '926', '7AD', 'C4E', 'FFF'],
    ['E2E', '323', '6D2', '976', '83F', 'C96'],
    ['9E9', 'A8B', '9C1', '461', 'F74', 'D05'],
    ['EDD', 'E94', '5F4', 'D1D', 'D03', 'DE3'],
    ['89', '925', 'CF9', 'CA0', 'F18', '4D2']
]

# Initialize number matrix
number_matrix = []
for row in range(len(hex_grid)):
    number_matrix.append([])
for row in number_matrix:
    for col in range(len(hex_grid[0])):
        row.append(None)

for row in range(len(hex_grid)):
    for col in range(len(hex_grid[0])):
        number_matrix[row][col] = get_hex(row, col)

# Initialize path plots,
# with vertices labeled according to row and column numbers (ex: R0C0)
# Only considers moving down or right along matrix
path_plot = {}
for row in range(len(number_matrix)):
    for col in range(len(number_matrix[0])):
        vertex = "R%dC%d" % (row, col)
        paths = {}
        try:
            paths.update({
                "R%dC%d" % (row+1, col): number_matrix[row+1][col]
            })
        except IndexError:
            pass
        try:
            paths.update({
                "R%dC%d" % (row, col+1): number_matrix[row][col+1]
            })
        except IndexError:
            pass
        path_plot.update({
            vertex: paths
        })

start = "R0C0"
end = "R%dC%d" % (len(number_matrix)-1, len(number_matrix[0])-1)

print dijkstra(path_plot, start, end)
