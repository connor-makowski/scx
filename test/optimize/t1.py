from scx.optimize import Model

# Create variables
sugary_amt = Model.variable(name="sugary", lowBound=0)
regular_amt = Model.variable(name="regular", lowBound=0)

# Initialize the model
model = Model(name="Crazy_Cereal", sense="maximize")

# Add the Objective Fn
model.add_objective(fn=(sugary_amt * 0.94) + (regular_amt * 0.82))

# Add Constraints
model.add_constraint(
    name="sugar_constraint", fn=sugary_amt * 0.66 + regular_amt * 0.21 <= 2000
)
model.add_constraint(
    name="corn_flake_constraint",
    fn=sugary_amt * 0.34 + regular_amt * 0.79 <= 4000,
)

# Solve the model
model.solve(get_duals=True, get_slacks=True)

if round(model.outputs.get("objective"), 2) != 5117.33:
    print("optimize/t1.py failed")
