import gurobipy as gp
from gurobipy import GRB

# Define data
supply = [1000, 1500, 1200]  # Supply nodes
demand = [2300, 1400]  # Demand nodes
cost = [
    [80, 215],
    [100, 108],
    [102, 68]
]  # Cost of transportation from supply i to demand j

m = gp.Model()
# Define decision variables
flow = m.addVars(3, 2, lb=0, vtype=GRB.INTEGER, name="flow")

# Define supply constraints
for i in range(3):
    m.addConstr(gp.quicksum(flow[i, j] for j in range(2)) <= supply[i], name=f"supply_{i}")


# Define demand constraints
for j in range(2):
    m.addConstr(gp.quicksum(flow[i, j] for i in range(3)) >= demand[j], name=f"demand_{j}")

m.setObjective(gp.quicksum(flow[i, j] * cost[i][j] for i in range(3) for j in range(2)), sense=GRB.MINIMIZE)

m.optimize()

# Print results
if m.status == GRB.OPTIMAL:
    print(f"Optimal solution found with objective value {m.objVal:.2f}")
    for i in range(3):
        for j in range(2):
            if flow[i, j].x > 0:
                print(f"Flow from supply node {i+1} to demand node {j+1}: {flow[i, j].x:.0f}")
else:
    print("No solution found.")