from pamda import pamda
from scx.optimize import Model

# A sudoku model

# Create variables
data = [{
        'row':row+1,
        'col':col+1,
        'box':int(row/3)*3+int(col/3)+1,
        'value':value+1,
        'use':Model.variable(name=f"sq_{row+1}_{col+1}_{value+1}", cat="Binary")
    } for row in range(9) for col in range(9) for value in range(9)]

constraints=[
    {'row':1, 'col':1, 'value':7},
    {'row':1, 'col':2, 'value':6},
]

# Initialize the model
model = Model(name="Sudoku", sense=None)


## Ensure that each square gets assigned exactly one value
for i in pamda.groupKeys(['row','col'], data):
    model.add_constraint(
        Model.sum(pamda.pluck('use',i))==1
    )

## Add in constraints such that each row, col and box will only have a value once
for var in ['row','col','box']:
    for i in pamda.groupKeys([var,'value'], data):
        model.add_constraint(
            Model.sum(pamda.pluck('use',i))==1
        )

# Add in constraints such that each square must match the provided inputs
nested_data=pamda.nest(['row','col','value'],'use', data)
for j in constraints:
    model.add_constraint(
        nested_data[j['row']][j['col']][j['value']][0]==1
    )


# Solve the model
model.solve()


used = [i for i in data if (i['use'].value())==1]
for key, value in pamda.nest(['row','col'],'value',used).items():
    print(key, value)
