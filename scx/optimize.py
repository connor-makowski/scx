import pulp
import type_enforced
from .utils import Error


@type_enforced.Enforcer
def Variable(*args, name: str = None, **kwargs):
    return pulp.LpVariable(*args, name=name, **kwargs)


@type_enforced.Enforcer
class Model(Error):
    def __init__(self, name: str, type: str):
        # Validation Attributes
        self.__solved__ = False
        self.__objective_added__ = False

        # Standard attributes
        self.name = name
        self.outputs = {"status": "Not Solved"}

        # Create PuLP Model
        if type.lower() == "maximize":
            self.model = pulp.LpProblem(name=self.name, sense=pulp.LpMaximize)
        elif type.lower() == "minimize":
            self.model = pulp.LpProblem(name=self.name, sense=pulp.LpMinimize)
        else:
            self.exception(
                "When creating a model, `type` must be specified as either `maximize` or `minimize`."
            )

    def add_objective(self, fn):
        # Validity Checks
        if self.__objective_added__:
            self.exception("An objective function has already been added to this model.")

        # Add the objective function to the model
        self.model += fn

        # Update the __objective_added__ validation attribute
        self.__objective_added__ = True

    def add_constraint(self, fn, name: [str, type(None)] = None):
        # Validity Checks
        if not self.__objective_added__:
            self.exception(
                "An objective function should be added to this model before adding constraints."
            )
        if self.__solved__:
            self.exception(
                "This model has already been solved. You can not add any more constraints."
            )

        # Add the constraint to the model
        if name != None:
            self.model += (fn, name)
        else:
            self.model += fn

    def solve(self, pulp_log: bool = False, except_on_infeasible: bool = True):
        if self.__solved__:
            self.exception(
                "This model has already been solved. You can not add any more constraints."
            )
        # Solve the model
        self.model.solve(pulp.PULP_CBC_CMD(msg=(3 if pulp_log else 0)))

        if self.model.status == -1:
            if except_on_infeasible:
                self.exception("The current model is infeasible and can not be solved.")
            else:
                self.warn(
                    "The current model is infeasible and can not be solved. Constraints have been relaxed to provide a solution anyway."
                )
        self.__solved__ = True
        self.outputs = {
            "status": f"{pulp.LpStatus[self.model.status]}",
            "objective": self.model.objective.value(),
            "variables": {i.name: i.value() for i in self.model.variables()},
        }
