from scx.optimize import Model


# Generic Problem
# Create variables
product_1_amt = Model.variable(name="product_1", lowBound=0)
product_2_amt = Model.variable(name="product_1", lowBound=0)

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

# Two variables are the same name this should fail in order to pass.
try:
    model.solve()
    print("optimize/t5.py failed")
except:
    pass
