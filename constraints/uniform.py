from contraintes.constraints._base import ConstraintsObject
import numpy as np


class UniformConstraintsGenerator(ConstraintsObject):
    """
    Generate constraints uniformly

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features), default = None
        The data
    y : array-like of shape (n_samples,), default = None
        The labels
    """


    def __init__(self, X=None, y=None):
        super().__init__()

        self.X = X
        self.y = y

        if X is not None:
            self.ids = np.arange(len(X))
        elif y is not None:
            self.ids = np.arange(len(y))
        else:
            raise ValueError("Either X or y must be provided")


    def generate_must_link(self, nb_constraints, with_replacement=False, based_on_y=True, no_tautology=False):
        """
        Generate must link constraints

        Parameters
        ----------
        nb_constraints : int
            The number of constraints to generate
        with_replacement : bool, default = False
            If True, the same point can have multiple constraints
        based_on_y : bool, default = True
            If True, the constraints are generated based on the labels
        no_tautology : bool, default = False
            If True, the constraints are generated without tautology, i.e. a point cannot be linked to itself
        """

        points_to_constraint = set(np.choice(self.ids, nb_constraints, replace=with_replacement))
        
        if based_on_y:
            assert self.y is not None, "y is not definded"

            for c_a in points_to_constraint:

                c_b = np.choice(np.where(self.y == self.y[c_a]), 1)
                if no_tautology:
                    while c_a == c_b:
                        c_b = np.choice(np.where(self.y == self.y[c_a]), 1)

                self.add_must_link(c_a, c_b)
        else:
            for c_a in points_to_constraint:

                if no_tautology:
                    c_b = np.choice(points_to_constraint - {c_a}, 1)
                else:
                    c_b = np.choice(points_to_constraint, 1)

                self.add_must_link(c_a, c_b)

    def generate_cannot_link(self, nb_constraints, with_replacement=False, based_on_y=True):
        """
        Generate cannot link constraints

        Parameters
        ----------
        nb_constraints : int
            The number of constraints to generate
        with_replacement : bool, default = False
            If True, the same point can have multiple constraints
        based_on_y : bool, default = True
            If True, the constraints are generated based on the labels
        """

        points_to_constraint = set(np.choice(self.ids, nb_constraints, replace=with_replacement))
        
        if based_on_y:
            assert self.y is not None, "y is not definded"

            for c_a in points_to_constraint:

                c_b = np.choice(np.where(self.y != self.y[c_a]), 1)

                self.add_cannot_link(c_a, c_b)
        else:
            for c_a in points_to_constraint:

                c_b = np.choice(points_to_constraint - {c_a}, 1)

                self.add_cannot_link(c_a, c_b)

