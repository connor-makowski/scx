from scx.optimize import Model


# Generic Problem
# Create variables
product_1_amt = Model.variable(name="product_1", lowBound=0)
product_2_amt = Model.variable(name="product_2", lowBound=0)

# Initialize the model
model = Model(name="Generic_Problem", sense="maximize")

# Add the Objective Fn
model.add_objective(fn=(product_1_amt * 1) + (product_2_amt * 1))

# Add Constraints
model.add_constraint(
    name="input_1_constraint", fn=product_1_amt * 1 + product_2_amt * 2 <= 100
)
model.add_constraint(
    name="input_2_constraint", fn=product_1_amt * 3 + product_2_amt * 1 <= 200
)

# Solve the model
model.solve(get_duals=True, get_slacks=True)

if round(model.outputs.get("objective"), 2) != 80.00:
    print("optimize/t4a.py failed")
