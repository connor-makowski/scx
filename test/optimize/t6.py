from scx.optimize import Model

# Create variables
data = {
    "sugary": {
        "sugar": 0.66,
        "corn_flakes": 0.34,
        "profit": 0.94,
        "amt": Model.variable(name="sugary", lowBound=0),
    },
    "regular": {
        "sugar": 0.21,
        "corn_flakes": 0.79,
        "profit": 0.82,
        "amt": Model.variable(name="regular", lowBound=0),
    },
}

constraints = {"sugar": 2000, "corn_flakes": 4000}

# Initialize the model
model = Model(name="Crazy_Cereal", sense="maximize")


# Add the Objective Fn
model.add_objective(
    fn=Model.sum([i["amt"] * i["profit"] for i in data.values()])
)

# Add Constraints
for key, value in constraints.items():
    model.add_constraint(
        name=f"{key}_constraint",
        fn=Model.sum([i["amt"] * i[key] for i in data.values()]) <= value,
    )

try:
    model.get_formulation()
    model.solve()
except:
    print("optimize/t6.py failed")
