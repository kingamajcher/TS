import random
from igraph import Graph

# bandwidth - przepustowość
# capacity - przepustowość całości
# flow - przepływ
# reliability - niezawodność
# adjacency - sąsiedztwo

# function for loading matrix from file
def load_matrix(filename):
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            row = [float(x) for x in line.replace(',', '').split()]
            matrix.append(row)
    return matrix

# function for adding atribute to graph
def add_attribute_to_graph(graph, attribute, values):
    for i, row in enumerate(values):
        for j, value in enumerate(row):
            if value > 0:
                graph.es.find(_source=i, _target=j)[attribute] = value

# function to get graph
def get_graph(matrix):
    return Graph.Adjacency(matrix)

# function for counting paths
def count_paths(graph, i, j, intensity_matrix, flow_matrix):
    shortest_path = graph.get_shortest_paths(i, to=j, mode='OUT', output='vpath')
    if shortest_path[0]:
        x = shortest_path[0][0]
        for path in shortest_path[0][1:]:
            flow_matrix[x][path] += intensity_matrix[i][j]
            x = path

# function for calculating bandwidth
def calculate_bandwidth(N, value):
    n = 20
    capacity = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if N[i][j] > 0:
                capacity[i][j] = value
    return capacity

# function for calculating flow
def calculate_flow(graph, intensity_matrix):
    n = 20
    flow_matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                count_paths(graph, i, j, intensity_matrix, flow_matrix)
                count_paths(graph, j, i, intensity_matrix, flow_matrix)
    return flow_matrix

# function for calculating reliability
def calculate_reliability(graph, T_max, m, sum):
    results = 0
    for edge in graph.es:
        a_function = edge.attributes()["flow"]
        c_function = edge.attributes()["bandwidth"]
        term = a_function / ((c_function / m) - a_function)
        if term < 0:
            return "overflow"
        results += term
    T = results / sum
    return T < T_max

# function for increasing flow (multiplies flow by M)
def increase_flow(graph_flow, M):
    for i in range(20):
        for j in range(20):
            graph_flow[i][j] *= M
    return graph_flow

# function for increasing bandwidth (multiplies bandwidth by M)
def increase_bandwidth(graph_bandwidth, M):
    for i in range(20):
        for j in range(20):
            graph_bandwidth[i][j] *= M
    return graph_bandwidth

# function for checking reliability
def check_reliability(p):
    ran = random.random()
    return ran <= p

# test 1 - changing the probability of failure of edge of graph
def test1(N, p, T_max, intensity_matrix, m, capacity):
    for i in range(20):
        for j in range(i, 20):
            if not check_reliability(p):
                N[i][j] = 0
                N[j][i] = 0

    graph = get_graph(N)

    if not graph.is_connected():
        return "unconnected"

    graph_flow = calculate_flow(graph, intensity_matrix)
    add_attribute_to_graph(graph, "flow", graph_flow)

    graph_bandwidth = calculate_bandwidth(N, capacity)
    add_attribute_to_graph(graph, "bandwidth", graph_bandwidth)

    sum_t = sum(sum(x) for x in intensity_matrix)
    
    results = calculate_reliability(graph, T_max, m, sum_t)

    return results

# test 2 - checking the probability of failure by increasing values in flow matrix
def test2(N, p, T_max, intensity_matrix, m, capacity, M):

    for i in range(20):
        for j in range(i, 20):
            if not check_reliability(p):
                N[i][j] = 0
                N[j][i] = 0

    graph = get_graph(N)

    if not graph.is_connected():
        return "unconnected"

    graph_flow = calculate_flow(graph, intensity_matrix)
    graph_flow = increase_flow(graph_flow, M)
    add_attribute_to_graph(graph, "flow", graph_flow)

    graph_bandwidth = calculate_bandwidth(N, capacity)
    add_attribute_to_graph(graph, "bandwidth", graph_bandwidth)

    sum_t = sum(sum(x) for x in intensity_matrix)

    results = calculate_reliability(graph, T_max, m, sum_t)

    return results

# test 3 - checking the probability of failure by increasing values in bandwidth matrix
def test3(N, p, T_max, intensity_matrix, m, capacity, M):

    for i in range(20):
        for j in range(i, 20):
            if not check_reliability(p):
                N[i][j] = 0
                N[j][i] = 0

    graph = get_graph(N)

    if not graph.is_connected():
        return "unconnected"

    graph_flow = calculate_flow(graph, intensity_matrix)
    add_attribute_to_graph(graph, "flow", graph_flow)

    graph_bandwidth = calculate_bandwidth(N, capacity)
    graph_bandwidth = increase_bandwidth(graph_bandwidth, M)
    add_attribute_to_graph(graph, "bandwidth", graph_bandwidth)

    sum_t = sum(sum(x) for x in intensity_matrix)

    results = calculate_reliability(graph, T_max, m, sum_t)

    return results

# test 4 - checking the probability of failure by increasing the number of edges in adjacency matrix
def test4(N, p, T_max, intensity_matrix, m, capacity, K):
    for k in range(K):
        source_vertex = random.randint(0, 19)
        target_vertex = random.randint(0, 19)
        while source_vertex == target_vertex or N[source_vertex][target_vertex] == 1:
            source_vertex = random.randint(0, 19)
            target_vertex = random.randint(0, 19)
        N[source_vertex][target_vertex] = 1
        N[target_vertex][source_vertex] = 1

    for i in range(20):
        for j in range(i, 20):
            if not check_reliability(p):
                N[i][j] = 0
                N[j][i] = 0

    graph = get_graph(N)

    if not graph.is_connected():
        return "unconnected"

    graph_flow = calculate_flow(graph, intensity_matrix)
    add_attribute_to_graph(graph, "flow", graph_flow)

    graph_bandwidth = calculate_bandwidth(N, capacity)
    add_attribute_to_graph(graph, "bandwidth", graph_bandwidth)

    sum_t = sum(sum(x) for x in intensity_matrix)
    
    results = calculate_reliability(graph, T_max, m, sum_t)

    return results



def main():
    n = 10000
    p = 0.9 # probability of network not failing
    T_max = 0.0001 # maximum time
    m = 1200  # size of a packet
    capacity = 1456777601  # maximum capacity

    unconnected = 0
    overflow = 0
    success = 0

    intensity_matrix = load_matrix("intensity_matrix.txt")
    tested_matrix = load_matrix("adjacency_matrix.txt")

    for i in range(n):
        tested_matrix = load_matrix("adjacency_matrix.txt")
        result = test1(tested_matrix, p, T_max, intensity_matrix, m, capacity)
        if result == "unconnected":
            unconnected += 1
        elif result == "overflow":
            overflow += 1
        elif result:
            success += 1

    print(f"Test 1:\n" +
        f"p = {p},\n" +
        f"Success: {success}, ({success / n * 100})%,\n" +
        f"Unconnected: {unconnected},\n" +
        f"Overflow: {overflow},\n" +
        f"T > T_max: {n - success - unconnected - overflow} \n")

    unconnected = 0
    overflow = 0
    success = 0


    M = 1.2

    for i in range(n):
        tested_matrix = load_matrix("adjacency_matrix.txt")
        result = test2(tested_matrix, p, T_max, intensity_matrix, m, capacity, M)
        if result == "unconnected":
            unconnected += 1
        elif result == "overflow":
            overflow += 1
        elif result:
            success += 1

    print(f"Test 2:\n" +
        f"M = {M},\n" +
        f"Success: {success}, ({success / n * 100})%,\n" +
        f"Unconnected: {unconnected},\n" +
        f"Overflow: {overflow},\n" +
        f"T > T_max: {n - success - unconnected - overflow}\n")

    unconnected = 0
    overflow = 0
    success = 0


    M = 10
    capacity = 146777601

    for i in range(n):
        tested_matrix = load_matrix("adjacency_matrix.txt")
        result = test3(tested_matrix, p, T_max, intensity_matrix, m, capacity, M)
        if result == "unconnected":
            unconnected += 1
        elif result == "overflow":
            overflow += 1
        elif result:
            success += 1

    print(f"Test 3:\n" +
        f"M = {M},\n" +
        f"Success: {success}, ({success / n * 100})%,\n" +
        f"Unconnected: {unconnected},\n" +
        f"Overflow: {overflow},\n" +
        f"T > T_max: {n - success - unconnected - overflow}\n")
    
    unconnected = 0
    overflow = 0
    success = 0


    capacity = 1456777601
    K = 5
    for i in range(n):
        tested_matrix = load_matrix("adjacency_matrix.txt")
        result = test4(tested_matrix, p, T_max, intensity_matrix, m, capacity, K)
        if result == "unconnected":
            unconnected += 1
        elif result == "overflow":
            overflow += 1
        elif result:
            success += 1

    print(f"Test 4:\n" +
        f"K = {K},\n" +
        f"Success: {success}, ({success / n * 100})%,\n" +
        f"Unconnected: {unconnected},\n" +
        f"Overflow: {overflow},\n" +
        f"T > T_max: {n - success - unconnected - overflow}\n")

    unconnected = 0
    overflow = 0
    success = 0


if __name__ == "__main__":
    main()
