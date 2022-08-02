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
    def __init__(self, name: str, sense: [str, type(None)]):
        """
        Initialize a new optimization model object.

        Requires:

        - `name`:
            - Type: str
            - What: The name of this optimization model
        - `sense`:
            - Type: str
            - What: The type of optimization to perform
            - Options: ['maximize','minimize',None]
            - Note: If None, no optimization is performed, but a feasible solution is searched for given the constraints
        """
        # Validation Attributes
        self.__solved__ = False
        self.__objective_added__ = False

        # Standard attributes
        self.name = name
        self.sense = sense
        self.outputs = {"status": "Not Solved"}

        # Create PuLP Model
        if sense == None:
            self.model = pulp.LpProblem(name=self.name)
            self.__objective_added__ = True
        elif sense.lower() == "maximize":
            self.model = pulp.LpProblem(name=self.name, sense=pulp.LpMaximize)
        elif sense.lower() == "minimize":
            self.model = pulp.LpProblem(name=self.name, sense=pulp.LpMinimize)
        else:
            self.exception(
                "When creating a model, `sense` must be specified as either `'maximize'`, `'minimize'` or `None`."
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
            if self.sense == None:
                self.exception(
                    "Models with `sense=None` should not have an objective function."
                )
            else:
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

    def solve(
        self,
        pulp_log: bool = False,
        except_on_infeasible: bool = True,
        get_duals: bool = False,
        get_slacks: bool = False,
    ):
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
        - `get_duals`:
            - Type: bool
            - What: A flag to indicate if the dual values for constraints should be added to the normal `outputs`.
            - Default: False
        - `get_slacks`:
            - Type: bool
            - What: A flag to indicate if the slack values for constraints should be added to the normal `outputs`.
            - Default: False
        """
        # Check the model validity
        self.validity_checks()
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
            "objective": self.model.objective.value()
            if self.sense != None
            else None,
            "variables": {i.name: i.value() for i in self.model.variables()},
        }
        if get_duals:
            self.get_duals()
        if get_slacks:
            self.get_slacks()

    def get_slacks(self):
        """
        Adds slack values to the model outputs dictionary as `slacks` and also returns those slack values as an dictonary.

        Notes:

            - The model must be solved before this method can be used
            - Slack values might not be avaialable depending on the solver that is used
        """
        if not self.__solved__:
            self.exception(
                "The current model must be solved before getting slacks."
            )
        self.outputs["slacks"] = {
            key: value.slack for key, value in self.model.constraints.items()
        }
        return self.outputs["slacks"]

    def get_duals(self):
        """
        Adds dual values to the model outputs dictionary as `duals` and also returns those dual values as an dictonary.

        Notes:

            - The model must be solved before this method can be used
            - Dual values will be 0 or None for non LP models (EG MILPs)
            - Dual values might not be avaialable depending on the solver that is used
        """
        if not self.__solved__:
            self.exception(
                "The current model must be solved before getting duals."
            )
        self.outputs["duals"] = {
            key: value.pi for key, value in self.model.constraints.items()
        }
        return self.outputs["duals"]

    def validity_checks(self):
        """
        Runs validity checks on the model before solving it

        - Checks to make sure the model has not already been solved
        - Ensures that variables each have unique names
        - Note: PuLP automatically verifies constraint name uniqueness
        """
        # Ensure model is not solved
        if self.__solved__:
            self.exception(
                "This model has already been solved. You can not add any more constraints."
            )
        # Ensure Variable Names are Unique
        variable_names = [i.name for i in self.model.variables()]
        if len(set(variable_names)) < len(variable_names):
            self.exception("Overlapping variable names exist in the model.")

    def get_formulation(self):
        """
        Returns the current model formulation as a string in a human readable form.

        Note: This aggregate variables where possible such that `variable_1*2 + variable_1*1` => `variable_1*3`
        """
        return str(self.model)
