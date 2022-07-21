SCx
==========
MIT's Supply Chain Micromaster (SCx) Python Package

# Documentation
[Technical documentation](https://connor-makowski.github.io/scx/index.html) can be found [here](https://connor-makowski.github.io/scx/index.html).

## Local Setup
Make sure you have Python 3.6.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).
- Recommended (but Optional) - Setup and activate a virtual environment:  
  - Install (or upgrade) virtualenv:
  ```
  python3 -m pip install --upgrade virtualenv
  ```
  - Create your virtualenv named `venv`:
  ```
  python3 -m virtualenv venv
  ```
  - Activate your virtual environment
    - On Unix (Mac or Linux):
    ```
    source venv/bin/activate
    ```
    - On Windows:
    ```
    venv\scripts\activate
    ```
- Then in your terminal:
  - `pip install scx`

## Cloud Setup
Create a google account and access google colab [here](https://colab.research.google.com/).
- Create a new notebook
- Install the `scx` package by adding the following to a new cell and running it:
  - `pip install scx`

# Getting Started

## Basic Usage
```py
from scx.optimize import Model
```

## Examples

### Simple Optimization
```py
from scx.optimize import Model

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
```
Outputs:
```py
{'status': 'Optimal', 'objective': 80.0, 'variables': {'product_1': 60.0, 'product_2': 20.0}, 'duals': {'input_1_constraint': 0.4, 'input_2_constraint': 0.2}, 'slacks': {'input_1_constraint': -0.0, 'input_2_constraint': -0.0}}
```

### Array Based Optimization
```py
from scx.optimize import Model

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
```
Outputs:
```py
{'status': 'Optimal', 'objective': 80.0, 'variables': {'product_1': 60.0, 'product_2': 20.0}, 'duals': {'input_1_constraint': 0.4, 'input_2_constraint': 0.2}, 'slacks': {'input_1_constraint': -0.0, 'input_2_constraint': -0.0}}
```
