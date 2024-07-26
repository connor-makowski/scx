# SCx
[![PyPI version](https://badge.fury.io/py/scx.svg)](https://badge.fury.io/py/scx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MIT's [Supply Chain Micromaster](https://micromasters.mit.edu/scm/) (SCx) Python Package

## Documentation
[Technical documentation](https://connor-makowski.github.io/scx/scx.html) can be found [here](https://connor-makowski.github.io/scx/scx.html).

## Examples
- [All Optimization Examples](https://github.com/connor-makowski/scx/tree/main/notebooks/optimization/)
  - [Basic Examples](https://github.com/connor-makowski/scx/tree/main/notebooks/optimization/basic_examples)
  - [Blinky Examples (with video walkthroughs)](https://github.com/connor-makowski/scx/tree/main/notebooks/optimization/blinky_examples)
  - [Food On Wheels Examples (with video walkthroughs)](https://github.com/connor-makowski/scx/tree/main/notebooks/optimization/fow_examples)
  - [Eco Pants Examples (with video walkthroughs)](https://github.com/connor-makowski/scx/tree/main/notebooks/optimization/eco_pants_examples)
  - [Miscellaneous Examples](https://github.com/connor-makowski/scx/tree/main/notebooks/optimization/misc_examples)
- [All Database Examples](https://github.com/connor-makowski/scx/tree/main/notebooks/database/)
  - [Transaction Database Example](https://github.com/connor-makowski/scx/tree/main/notebooks/database/Transaction.ipynb)

## Setup

### Cloud Setup (Google Colab)
- You can access google colab [here](https://colab.research.google.com/)
- Create a new notebook
- Install the `scx` package by adding the following to a new code cell at the **top** of your notebook and running it:
  - `pip install scx`


### Local Setup
Make sure you have Python 3.7.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).
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

## Optimization Getting Started
See all of the optimization examples [here](https://github.com/connor-makowski/scx/tree/main/notebooks/optimization/).

### Basic Usage
```py
from scx.optimize import Model
```

#### Simple Optimization
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

## Database Getting Started
See all of the database examples [here](https://github.com/connor-makowski/scx/tree/main/notebooks/database/)

### Basic Usage
```py
from scx.database import Database
# Specify the S3 path to the data
data_folder = 's3://scx-dev/databases/supermarket/'
# Create the database
db = Database(f"""
    CREATE TABLE Customers AS SELECT * FROM read_parquet('{data_folder}customers.parquet');
""")
# Show the database Schema
db.show_info()

# Query the database
db.query("SELECT * FROM Customers LIMIT 5")
```