import pulp, type_enforced
from .utils import Error


@type_enforced.Enforcer
class ModelUtils(Error):
    @staticmethod
    def variable(
        name: str,
        lowBound: [float, int, type(None)] = None,
        upBound: [float, int, type(None)] = None,
        cat: str = "Continuous",
    ):
        """
        Creates a variable object to be used in an optimize.Model object

        Requires:

        - `name`:
            - Type: str
            - What: The name of this variable

        Optional:

        - `lowBound`:
            - Type: int | float
            - What: A lower bound for this variable
            - Default: -infinity
        - `upBound`:
            - Type: int | float
            - What: An upper bound for this variable
            - Default: infinity
        - `cat`:
            - Type: str
            - What: The category of this variable
            - Default: `Continuous`
            - Options: ['Continuous','Binary','Integer']
        """
        kwargs = {"name": name, "cat": cat}
        if lowBound is not None:
            kwargs["lowBound"] = lowBound
        if upBound is not None:
            kwargs["upBound"] = upBound
        return pulp.LpVariable(**kwargs)

    @staticmethod
    def sum(vector: list):
        """
        Creates a function that can sum over a list to add as an objective or constraint on the model

        Requires:

        - `vector`:
            - Type: list
            - What: A list of items or functions to sum over
        """
        return pulp.lpSum(vector)


@type_enforced.Enforcer
class Model(ModelUtils):
    def __init__(self, name: str, type: str):
        """
        Initialize a new optimization model object.

        Requires:

        - `name`:
            - Type: str
            - What: The name of this optimization model
        - `type`:
            - Type: str
            - What: The type of optimization to perform
            - Options: ['maximize','minimize']
        """
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
        """
        Add the objective function to the current model object. Each model can only have one objective function.

        Requires:

        - `fn`:
            - Type: function
            - What: The pythonic version of the objective function
            - Note: This function should **not** have any pythonic [comparison operators](https://docs.python.org/3/reference/expressions.html#comparisons)
        """
        # Validity Checks
        if self.__objective_added__:
            self.exception(
                "An objective function has already been added to this model."
            )

        # Add the objective function to the model
        self.model += fn

        # Update the __objective_added__ validation attribute
        self.__objective_added__ = True

    def add_constraint(self, fn, name: [str, type(None)] = None):
        """
        Add a constraint function to the current model object. Each model can have unlimited constraints.

        Requires:

        - `fn`:
            - Type: function
            - What: The pythonic version of the objective function
            - Note: This function should have pythonic [comparison operators](https://docs.python.org/3/reference/expressions.html#comparison)

        Optional:

        - `name`:
            - Type: str
            - What: The name of this constraint
            - Default: None


        """
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
        """
        Solve the current model object.

        Optional:

        - `pulp_log`:
            - Type: bool
            - What: A flag to indicate if the relevant pulp / coinOr solver log should be logged in the console. This can be helpful for debugging.
            - Default: False
        - `except_on_infeasible`:
            - Type: bool
            - What: A flag to indicate if the model should throw an exception if the optimization model is infeasible. If false, the model will automatically relax constraints to generate an infeasible solution.
            - Default: True
        """
        if self.__solved__:
            self.exception(
                "This model has already been solved. You can not add any more constraints."
            )
        # Solve the model
        self.model.solve(pulp.PULP_CBC_CMD(msg=(3 if pulp_log else 0)))

        if self.model.status == -1:
            if except_on_infeasible:
                self.exception(
                    "The current model is infeasible and can not be solved."
                )
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
