from scx.optimize import Model, Variable

# Create variables
sugary_amt = Variable(name="sugary", lowBound=0)
regular_amt = Variable(name="regular", lowBound=0)

# Initialize the model
model = Model(name="Crazy_Cereal", type='maximize')

# Add the Objective Fn
model.add_objective(
    fn=(sugary_amt*.94)+(regular_amt*.82)
)

# Add Constraints
model.add_constraint(
    name='sugar_constraint',
    fn=sugary_amt*.66+regular_amt*.21 <= 2000
)
model.add_constraint(
    name = 'corn_flake_constraint',
    fn = sugary_amt*.34+regular_amt*.79 <= 4000
)

# Solve the model
model.solve()

# Show the outputs
print(model.outputs)
