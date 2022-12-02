# Python Intro

This repository houses some introductory python notebooks to get people started learning python.

## Reference Use

To use these notebooks as reference materials, simply open up the .ipynb notebooks directly in github. All notebooks can be found in the `notebooks` folder:
- `notebooks/introduction`: A set of notebooks used to teach an introduction to python
- `notebooks/optimization`: A set of notebooks to teach optimization using the scx package

## Interactive Use

### Web (With Google Colab)
To use these notebooks on Google Colab, simply copy the link to your desired notebook and open it using the Github tab in the Google Colab file opener.

### On Your Machine (With Jupyter Notebooks)

## Local Setup

1. Download (or clone) this repository
2. Open a terminal in this cloned directory
3. Make sure you have Python 3.6.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).
4. Recommended (but Optional) - Setup and activate a virtual environment:  

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

5. In your terminal install jupyter notebooks:
```
python3 -m pip install jupyter
```
6. In your terminal:
  ```
  jupyter notebook
  ```
   - Browse in chrome to your desired notebooks.
