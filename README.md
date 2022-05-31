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
