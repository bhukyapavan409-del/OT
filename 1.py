import numpy as np

M = 1000000

c = np.array([3, 5, 0, 0, -M])



A = np.array([
    [1, 1, -1, 0, 1],
    [2, 1, 0, 1, 0]
], dtype=float)

b = np.array([4, 6], dtype=float)

variables = ["x1", "x2", "s1", "s2", "a1"]

basis = [4, 3]

tableau = np.zeros((3, 6))

tableau[:2, :5] = A
tableau[:2, 5] = b


cb = np.array([c[i] for i in basis])


zj = cb @ A


cj_zj = c - zj

print("Initial Tableau")
print("----------------")
print("Basis\tCb\tx1\tx2\ts1\ts2\ta1\tRHS")

for i in range(2):
    print(
        variables[basis[i]],
        "\t",
        cb[i],
        "\t",
        *tableau[i]
    )

print("Zj\t\t\t", *zj, "\t", cb @ b)
print("Cj-Zj\t\t\t", *cj_zj, "\t")



while True:

    cb = np.array([c[i] for i in basis])


    zj = cb @ A

   
    cj_zj = c - zj

    print("\nCurrent Tableau")
    print("----------------")

    print("Basis\tCb\tx1\tx2\ts1\ts2\ta1\tRHS")

    for i in range(2):
        print(
            variables[basis[i]],
            "\t",
            cb[i],
            "\t",
            *np.round(tableau[i], 4)
        )

    print("Zj\t\t\t", *np.round(zj, 4), "\t", round(cb @ b, 4))
    print("Cj-Zj\t\t\t", *np.round(cj_zj, 4))


   
    if max(cj_zj) <= 0:
        break

    entering = np.argmax(cj_zj)

    ratios = []

    for i in range(2):
        if A[i, entering] > 0:
            ratios.append(b[i] / A[i, entering])
        else:
            ratios.append(np.inf)

    leaving = np.argmin(ratios)

    if ratios[leaving] == np.inf:
        print("Unbounded solution.")
        break

    print(
        "\nEntering variable:",
        variables[entering]
    )

    print(
        "Leaving variable:",
        variables[basis[leaving]]
    )

   
    pivot = A[leaving, entering]

  
    A[leaving, :] = A[leaving, :] / pivot
    b[leaving] = b[leaving] / pivot

   
    for i in range(2):

        if i != leaving:

            factor = A[i, entering]

            A[i, :] = A[i, :] - factor * A[leaving, :]
            b[i] = b[i] - factor * b[leaving]

  
    basis[leaving] = entering

cb = np.array([c[i] for i in basis])

solution = np.zeros(5)

for i in range(2):
    solution[basis[i]] = b[i]

Z = c @ solution

print("\n==============================")
print("OPTIMAL SOLUTION")
print("==============================")

for i in range(5):
    print(variables[i], "=", round(solution[i], 4))

print("Maximum Z =", round(Z, 4))

if solution[4] > 0:
    print("\nProblem is infeasible.")
else:
    print("\nArtificial variable = 0")
    print("Therefore, the solution is feasible.")