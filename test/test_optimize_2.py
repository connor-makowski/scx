from scx.optimize import Model

# Create variables
data={
    'sugary':{
        'sugar':.66,
        'corn_flakes':.34,
        'profit':.94,
        'amt':Model.variable(name="sugary", lowBound=0)
    },
    'regular': {
        'sugar':.21,
        'corn_flakes':.79,
        'profit':.82,
        'amt':Model.variable(name="regular", lowBound=0)
    }
}

constraints = {
    'sugar': 2000,
    'corn_flakes': 4000
}

# Initialize the model
model = Model(name="Crazy_Cereal", type='maximize')


# Add the Objective Fn
model.add_objective(
    fn=Model.sum([i['amt']*i['profit'] for i in data.values()])
)

# Add Constraints
for key, value in constraints.items():
    model.add_constraint(
        name=f'{key}_constraint',
        fn=Model.sum([i['amt']*i[key] for i in data.values()]) <= value
    )

# Solve the model
model.solve()

# Show the outputs
print(model.outputs)
