from scx.optimize import Model

# A sudoku model

# Create variables
data = [{
        'row':row+1,
        'col':col+1,
        'box':(row//3)*3+(col//3)+1,
        'value':value+1,
        'use':Model.variable(name=f"sq_{row+1}_{col+1}_{value+1}", cat="Binary")
    } for row in range(9) for col in range(9) for value in range(9)]

constraints=[
    {'row':1, 'col':1, 'value':7},
    {'row':1, 'col':2, 'value':6},
]

# Initialize the my_model
my_model = Model(name="Sudoku", sense=None)


# Add the Objective Fn
## No is objective needed. We just need to solve for the constraints.

# Add Constraints

## Ensure that each square gets assigned exactly one value
for row_i in range(1,10):
    for col_j in range(1,10):
        my_model.add_constraint(
            Model.sum([d['use'] for d in data if d['row']==row_i and d['col']==col_j])==1
        )

## Add in constraints such that each row, col and box will only have a value once
for key_name in ['row','col','box']:
    for key_value in range(1,10):
        for data_value in range(1,10):
            my_model.add_constraint(
                Model.sum([d['use'] for d in data if d[key_name]==key_value and d['value']==data_value])==1
            )

# Add in constraints such that each square must match the provided inputs
for j in constraints:
    my_model.add_constraint(
        Model.sum([d['use'] for d in data if d['row']==j['row'] and d['col']==j['col'] and d['value']==j['value']])==1
    )


# Solve the my_model
my_model.solve()

matrix = [[0 for row in range(9)] for col in range(9)]
used = [i for i in data if (i['use'].value())==1]
for item in used:
  matrix[item['row']-1][item['col']-1]=item['value']

expected_matrix = [
 [7, 6, 9, 1, 5, 3, 4, 2, 8],
 [2, 3, 5, 9, 4, 8, 7, 6, 1],
 [1, 4, 8, 6, 2, 7, 5, 9, 3],
 [3, 8, 6, 5, 1, 4, 2, 7, 9],
 [9, 7, 2, 3, 8, 6, 1, 5, 4],
 [5, 1, 4, 2, 7, 9, 3, 8, 6],
 [4, 2, 1, 8, 9, 5, 6, 3, 7],
 [6, 9, 7, 4, 3, 2, 8, 1, 5],
 [8, 5, 3, 7, 6, 1, 9, 4, 2]
]
if matrix != expected_matrix:
    print('optimize/t3.py failed')
