from scx.optimize import Model

transport = [
    {
        "origin_name": "A1",
        "destination_name": "DC1",
        "distance": 190,
        "cost_per_mile": 0.04,
    },
    {
        "origin_name": "A2",
        "destination_name": "DC1",
        "distance": 150,
        "cost_per_mile": 0.04,
    },
    {
        "origin_name": "DC1",
        "destination_name": "R1",
        "distance": 15,
        "cost_per_mile": 0.08,
    },
    {
        "origin_name": "DC1",
        "destination_name": "R2",
        "distance": 59,
        "cost_per_mile": 0.08,
    },
    {
        "origin_name": "DC1",
        "destination_name": "R3",
        "distance": 79,
        "cost_per_mile": 0.08,
    },
    {
        "origin_name": "A1",
        "destination_name": "DC2",
        "distance": 15,
        "cost_per_mile": 0.04,
    },
    {
        "origin_name": "A2",
        "destination_name": "DC2",
        "distance": 36,
        "cost_per_mile": 0.04,
    },
    {
        "origin_name": "DC2",
        "destination_name": "R1",
        "distance": 135,
        "cost_per_mile": 0.08,
    },
    {
        "origin_name": "DC2",
        "destination_name": "R2",
        "distance": 45,
        "cost_per_mile": 0.08,
    },
    {
        "origin_name": "DC2",
        "destination_name": "R3",
        "distance": 129,
        "cost_per_mile": 0.08,
    },
]

demand = [
    {"name": "R1", "demand": 2500},
    {"name": "R2", "demand": 4350},
    {"name": "R3", "demand": 3296},
]

assembly = [
    {
        "name": "A1",
        "limit": 13000,
    },
    {
        "name": "A2",
        "limit": 3500,
    },
]

distribution_center = [
    {
        "name": "DC1",
        "fixed_cost": 11500,
    },
    {
        "name": "DC2",
        "fixed_cost": 15500,
    },
]

# Some number big enough...
M = 999999

for t in transport:
    # Create decision variables for each item in transport
    t["amt"] = Model.variable(
        name=f"{t['origin_name']}__{t['destination_name']}__amt", lowBound=0
    )
    # Calculate the variable cost of shipping for each item in tranport
    t["cost"] = t["distance"] * t["cost_per_mile"]

for dc in distribution_center:
    dc["use"] = Model.variable(name=f"{dc['name']}__use", cat="Binary")

# Initialize the my_model
my_model = Model(name="Blinky22", sense="minimize")


# Add the Objective Fn
my_model.add_objective(
    fn=(
        Model.sum([t["amt"] * t["cost"] for t in transport])
        + Model.sum(
            [dc["use"] * dc["fixed_cost"] for dc in distribution_center]
        )
    )
)

# Add Constraints
## Demand Constraint
for d in demand:
    my_model.add_constraint(
        name=f"{d['name']}__demand",
        fn=my_model.sum(
            [t["amt"] for t in transport if t["destination_name"] == d["name"]]
        )
        >= d["demand"],
    )

## Supply Constraint
for a in assembly:
    my_model.add_constraint(
        name=f"{a['name']}__assembly_supply",
        fn=my_model.sum(
            [t["amt"] for t in transport if t["origin_name"] == a["name"]]
        )
        <= a["limit"],
    )

## Conservation of Flow Constraint
for dc in distribution_center:
    my_model.add_constraint(
        name=f"{dc['name']}__conservation_of_flow",
        # Set inbound flows for the DC equal to outbound flows
        fn=my_model.sum(
            [t["amt"] for t in transport if t["destination_name"] == dc["name"]]
        )
        == my_model.sum(
            [t["amt"] for t in transport if t["origin_name"] == dc["name"]]
        ),
    )

## Linking Constraint
for dc in distribution_center:
    my_model.add_constraint(
        name=f"{dc['name']}__linking_constraint",
        # Set inbound flows for the DC equal to outbound flows
        fn=my_model.sum(
            [t["amt"] for t in transport if t["destination_name"] == dc["name"]]
        )
        <= M * dc["use"],
    )

try:
    # Solve my_model
    my_model.solve()
    my_model.get_formulation()
    my_model.get_outputs()
except:
    print("optimize/t7.py failed")
