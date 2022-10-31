SCx
==========
MIT's Supply Chain Micromaster (SCx) Python Package

# Documentation
[Technical documentation](https://connor-makowski.github.io/scx/index.html) can be found [here](https://connor-makowski.github.io/scx/index.html).

# Setup

## Cloud Setup (Google Colab)
- You can access google colab [here](https://colab.research.google.com/)
- Create a new notebook (or use this [example one](https://colab.research.google.com/github/connor-makowski/python_for_scx/blob/main/notebooks/optimization/Q1.ipynb))
- Install the `scx` package by adding the following to a new cell at the top of your notebook and running it:
  - `pip install scx`


## Local Setup
Make sure you have Python 3.6.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).
<details>
<summary>
Recommended (but Optional) -> Expand this section to setup and activate a virtual environment.
</summary>

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
</details>

```
pip install scx
```

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
my_model = Model(name="Generic_Problem", sense='maximize')

# Add the Objective Fn
my_model.add_objective(
    fn = (product_1_amt*1)+(product_2_amt*1)
)

# Add Constraints
my_model.add_constraint(
    name = 'input_1_constraint',
    fn = product_1_amt*1+product_2_amt*2 <= 100
)
my_model.add_constraint(
    name = 'input_2_constraint',
    fn = product_1_amt*3+product_2_amt*1 <= 200
)

# Solve the model
my_model.solve(get_duals=True, get_slacks=True)

# Show the outputs
# NOTE: outputs can be fetched directly as a dictionary with `my_model.get_outputs()`
my_model.show_outputs()
```
Outputs:
```py
{'duals': {'input_1_constraint': 0.4, 'input_2_constraint': 0.2},
 'objective': 80.0,
 'slacks': {'input_1_constraint': -0.0, 'input_2_constraint': -0.0},
 'status': 'Optimal',
 'variables': {'product_1': 60.0, 'product_2': 20.0}}

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
my_model = Model(name="Array_Problem", sense='maximize')


# Add the Objective Fn
my_model.add_objective(
    fn=Model.sum([i['amt']*i['profit'] for i in data])
)

# Add Constraints
for j in constraints:
    my_model.add_constraint(
        name=f'{j["name"]}_constraint',
        fn=Model.sum([i['amt']*i[j['name']] for i in data]) <= j['max_amt']
    )

# Solve the model
my_model.solve(get_duals=True, get_slacks=True)

# Show the outputs
# NOTE: outputs can be fetched directly as a dictionary with `model.get_outputs()`
my_model.show_outputs()
```
Outputs:
```py
{'duals': {'input_1_constraint': 0.4, 'input_2_constraint': 0.2},
 'objective': 80.0,
 'slacks': {'input_1_constraint': -0.0, 'input_2_constraint': -0.0},
 'status': 'Optimal',
 'variables': {'product_1': 60.0, 'product_2': 20.0}}
```

### Show a model formulation
```py
from scx.optimize import Model

# Create variables
product_1_amt = Model.variable(name="product_1", lowBound=0)
product_2_amt = Model.variable(name="product_2", lowBound=0)

# Initialize the model
my_model = Model(name="Generic_Problem", sense='maximize')

# Add the Objective Fn
my_model.add_objective(
    fn = (product_1_amt*1)+(product_2_amt*1)
)

# Add Constraints
my_model.add_constraint(
    name = 'input_1_constraint',
    fn = product_1_amt*1+product_2_amt*2 <= 100
)
my_model.add_constraint(
    name = 'input_2_constraint',
    fn = product_1_amt*3+product_2_amt*1 <= 200
)

# Show the model formulation
my_model.show_formulation()
```
Outputs:
```
Generic_Problem:
MAXIMIZE
1*product_1 + 1*product_2 + 0
SUBJECT TO
input_1_constraint: product_1 + 2 product_2 <= 100

input_2_constraint: 3 product_1 + product_2 <= 200

VARIABLES
product_1 Continuous
product_2 Continuous
```
