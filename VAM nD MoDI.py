import numpy as np

def vogel_approximation(cost, supply, demand):

    cost = np.array(cost, dtype=float)
    supply = supply.copy()
    demand = demand.copy()

    m, n = cost.shape
    allocation = np.zeros((m, n))

    while sum(supply) > 0 and sum(demand) > 0:

        row_penalty = []

        for i in range(m):
            if supply[i] > 0:
                values = [
                    cost[i][j]
                    for j in range(n)
                    if demand[j] > 0
                ]

                if len(values) >= 2:
                    values.sort()
                    penalty = values[1] - values[0]
                else:
                    penalty = values[0]

                row_penalty.append(penalty)
            else:
                row_penalty.append(-1)

        col_penalty = []

        for j in range(n):
            if demand[j] > 0:
                values = [
                    cost[i][j]
                    for i in range(m)
                    if supply[i] > 0
                ]

                if len(values) >= 2:
                    values.sort()
                    penalty = values[1] - values[0]
                else:
                    penalty = values[0]

                col_penalty.append(penalty)
            else:
                col_penalty.append(-1)

        max_row = max(row_penalty)
        max_col = max(col_penalty)

        if max_row >= max_col:

            i = row_penalty.index(max_row)

            available = [
                (cost[i][j], j)
                for j in range(n)
                if demand[j] > 0
            ]

            j = min(available)[1]

        else:

            j = col_penalty.index(max_col)

            available = [
                (cost[i][j], i)
                for i in range(m)
                if supply[i] > 0
            ]

            i = min(available)[1]

        quantity = min(supply[i], demand[j])

        allocation[i][j] = quantity

        supply[i] -= quantity
        demand[j] -= quantity

    return allocation


def modi_method(cost, allocation):

    cost = np.array(cost, dtype=float)

    m, n = cost.shape

    while True:

     
        occupied = []

        for i in range(m):
            for j in range(n):
                if allocation[i][j] > 0:
                    occupied.append((i, j))

        u = [None] * m
        v = [None] * n

        u[0] = 0

        changed = True

        while changed:

            changed = False

            for i, j in occupied:

                if u[i] is not None and v[j] is None:
                    v[j] = cost[i][j] - u[i]
                    changed = True

                elif v[j] is not None and u[i] is None:
                    u[i] = cost[i][j] - v[j]
                    changed = True

    
        delta = np.zeros((m, n))

        for i in range(m):
            for j in range(n):

                if allocation[i][j] == 0:
                    delta[i][j] = cost[i][j] - u[i] - v[j]
                else:
                    delta[i][j] = 0

        print("\nMODI Opportunity Cost Table:")
        print(np.round(delta, 2))

     
        if np.all(delta >= 0):

            print("\nSolution is optimal.")
            break

  
        entering = np.unravel_index(
            np.argmin(delta),
            delta.shape
        )

        print(
            "Entering cell:",
            entering
        )

      
        loop = find_loop(
            allocation,
            entering
        )

        if loop is None:
            print("Unable to find loop.")
            break

        print("Loop:", loop)

    
        plus = []
        minus = []

        for k in range(len(loop)):

            if k % 2 == 0:
                plus.append(loop[k])
            else:
                minus.append(loop[k])

        theta = min(
            allocation[i][j]
            for i, j in minus
        )

        for i, j in plus:
            allocation[i][j] += theta

        for i, j in minus:
            allocation[i][j] -= theta

    return allocation


def find_loop(allocation, start):

    m, n = allocation.shape

    occupied = []

    for i in range(m):
        for j in range(n):
            if allocation[i][j] > 0 or (i, j) == start:
                occupied.append((i, j))

    def search(path):

        current = path[-1]

        if len(path) >= 4 and current == start:
            return path

        i, j = current

        candidates = []

       
        for jj in range(n):
            if jj != j and (i, jj) in occupied:
                candidates.append((i, jj))

   
        for ii in range(m):
            if ii != i and (ii, j) in occupied:
                candidates.append((ii, j))

        for next_cell in candidates:

            if next_cell == start and len(path) >= 4:
                return path + [start]

            if next_cell not in path:

            
                prev = path[-1]

                if len(path) == 1:
                    valid = True
                else:
                    if prev[0] == next_cell[0]:
                        valid = path[-2][0] != prev[0]
                    else:
                        valid = path[-2][1] != prev[1]

                if valid:

                    result = search(path + [next_cell])

                    if result is not None:
                        return result

        return None

    return search([start])


def calculate_cost(cost, allocation):

    total = 0

    for i in range(len(cost)):
        for j in range(len(cost[0])):
            total += cost[i][j] * allocation[i][j]

    return total



cost = [
    [19, 30, 50, 10],
    [70, 30, 40, 60],
    [40, 8, 70, 20]
]

supply = [7, 9, 18]

demand = [5, 8, 7, 14]


print("====================================")
print("TRANSPORTATION PROBLEM")
print("VAM + MODI METHOD")
print("====================================")


allocation = vogel_approximation(
    cost,
    supply,
    demand
)

print("\nInitial Basic Feasible Solution")
print("--------------------------------")

print(np.array(allocation, dtype=int))


initial_cost = calculate_cost(
    cost,
    allocation
)

print("\nInitial Transportation Cost =", initial_cost)



allocation = modi_method(
    cost,
    allocation
)


print("\n====================================")
print("OPTIMAL SHIPMENT PLAN")
print("====================================")

print(np.array(allocation, dtype=int))


optimal_cost = calculate_cost(
    cost,
    allocation
)

print("\nMinimum Transportation Cost =", optimal_cost)


print("\nShipment Details:")

for i in range(len(cost)):
    for j in range(len(cost[0])):

        if allocation[i][j] > 0:

            print(
                "Source S" + str(i + 1),
                "-> Destination D" + str(j + 1),
                ":",
                int(allocation[i][j]),
                "units"
            )