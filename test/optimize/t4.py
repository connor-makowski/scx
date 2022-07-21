from scx.optimize import Model


# Generic Problem
# Create variables
product_1_amt = Model.variable(name="product_1", lowBound=0)
product_2_amt = Model.variable(name="product_2", lowBound=0)

# Initialize the model
model = Model(name="Generic_Problem", sense='maximize')

# Add the Objective Fn
model.add_objective(
    fn = (product_1_amt*1)+(product_2_amt*1)
)

# Add Constraints
model.add_constraint(
    name = 'input_1_constraint',
    fn = product_1_amt*1+product_2_amt*2 <= 100
)
model.add_constraint(
    name = 'input_2_constraint',
    fn = product_1_amt*3+product_2_amt*1 <= 200
)

# Solve the model
model.solve(get_duals=True, get_slacks=True)

# Show the outputs
print(model.outputs)



# Array Problem
# Create variables
data=[
    {
        'name': 'product_1',
        'input_1': 1,
        'input_2': 3,
        'profit': 1,
        'amt': Model.variable(name="product_1", lowBound=0)
    },
    {
        'name': 'product_2',
        'input_1': 2,
        'input_2': 1,
        'profit': 1,
        'amt': Model.variable(name="product_2", lowBound=0)
    }
]

constraints = [
    {
        'name':'input_1',
        'max_amt':100
    },
    {
        'name':'input_2',
        'max_amt':200
    }
]

# Initialize the model
model = Model(name="Array_Problem", sense='maximize')


# Add the Objective Fn
model.add_objective(
    fn=Model.sum([i['amt']*i['profit'] for i in data])
)

# Add Constraints
for j in constraints:
    model.add_constraint(
        name=f'{j["name"]}_constraint',
        fn=Model.sum([i['amt']*i[j['name']] for i in data]) <= j['max_amt']
    )

# Solve the model
model.solve(get_duals=True, get_slacks=True)

# Show the outputs
print(model.outputs)
