from scx.optimize import Model

distances = [
    [105, 256, 86],
    [240, 136, 198],
]
cost_per_mi = 0.12

demand = [2500, 4350, 3296]

assembly_plants = ["A1", "A2"]
demand_regions = ["R1", "R2", "R3"]

decision_variables = [
    [Model.variable(name=f"{a}__{d}__amt", lowBound=0) for d in demand_regions]
    for a in assembly_plants
]

# Initialize the model
my_model = Model(name="Blinky22", sense="minimize")

# Add the Objective Fn
my_model.add_objective(
    fn=Model.sum(
        [
            distances[i][j] * decision_variables[i][j] * cost_per_mi
            for i in range(len(assembly_plants))
            for j in range(len(demand_regions))
        ]
    ),
)

# Add the Constraints
## Demand Constraint
for j in range(len(demand_regions)):
    my_model.add_constraint(
        name=f"Constraint__{demand_regions[j]}",
        fn=Model.sum(
            [decision_variables[i][j] for i in range(len(assembly_plants))]
        )
        >= demand[j],
    )

try:
    # Solve my_model
    my_model.solve()
    my_model.get_formulation()
    my_model.get_outputs()
except:
    print("optimize/t8.py failed")
