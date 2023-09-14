import pycsp3


class ConstraintsObject:

    def __init__(self):
        self.must_link = []
        self.cannot_link = []

    def add_must_link(self, i, j):
        self.must_link.append((i, j))

    def add_cannot_link(self, i, j):
        self.cannot_link.append((i, j))

    def get_constraints(self):
        return {"must_link_constraints": str(self.must_link), "cannot_link_constraints": str(self.cannot_link)}

    def get_points(self):
        """
        Get the points involved in the constraints.

        Returns
        -------
        set
            The set of points involved in the constraints.
        """

        return list(set([i for i, j in self.must_link + self.cannot_link] + [j for i, j in self.must_link + self.cannot_link]))

    def is_respected(self, clustering, method="boolean", incremental=False):
        """
        Check if the constraints are respected by a clustering.

        Parameters
        ----------
        clustering : array-like of shape (n_samples,)
            The clustering to check. The value of the ith element is the cluster of the ith point.
        method : str, default = "boolean"
            The method to use to check the constraints. Can be "boolean" or "count".
        incremental : bool, default = False
            If True, the constraints are checked for each number of constraints. If False, the constraints are checked for the total number of constraints.

        Returns
        -------
        bool or dict or list of bool or list of dict
            If method is "boolean", True if the constraints are respected, False otherwise.
            If method is "count", the number of constraints that are not respected for each type of constraint, in total and the total number of constraints.
            If incremental is True, a list of the results for each number of constraints.
        """
        rep = []
        for ml_max, cl_max in self._generator_constraints(incremental=incremental):

            c_ml = 0
            for i, j in self.must_link[:ml_max]:
                if clustering[i] != clustering[j]:
                    if method == "boolean":
                        return False
                    elif method == "count":
                        c_ml += 1
                    else:
                        raise ValueError("Unknown method: {method}")

            c_cl = 0
            for i, j in self.cannot_link[:cl_max]:
                if clustering[i] == clustering[j]:
                    if method == "boolean":
                        return False
                    elif method == "count":
                        c_cl += 1
                    else:
                        raise ValueError("Unknown method: {method}")

            if method == "boolean":
                rep.append(True)
            elif method == "count":
                rep.append({"must_link": c_ml, "cannot_link": c_cl, "total": c_ml + c_cl, "nb_ML": len(self.must_link), "nb_CL": len(self.cannot_link), "nb_constraints": (len(self.must_link) + len(self.cannot_link)), "prop_ML": c_ml / len(self.must_link), "prop_CL": c_cl / len(self.cannot_link), "prop_total": (c_ml + c_cl) / (len(self.must_link) + len(self.cannot_link))})
            else:
                raise ValueError("Unknown method: {method}")
        
        if len(rep)==1:
            return rep[0]
        else:
            return rep

    def _generator_constraints(self, incremental=False):
        
        if incremental:
            ml = len(self.must_link)
            cl = len(self.cannot_link)

            mi = min(ml, cl)
            ma = max(ml, cl)

            i = 0
            j = 0
            flag=False
            while i < ma:
                if ml > cl:
                    yield i, j
                else:
                    yield j, i
                    
                if i % (ma // mi) == 0 and flag and j + 1 < mi:
                    j += 1
                    flag = False
                else: 
                    i += 1
                    flag = True
        else:
            yield len(self.must_link), len(self.cannot_link)
            
    def is_overconstrained(self, n_clusters=None):
        """
        Check if it is possible de respect all the constraints.

        Parameters
        ----------
        n_clusters : int, default = None
            The maximum number of clusters to consider. If None, the number of points is used.
        
        Returns
        -------
        bool
            True if it is impossible to respect all the constraints, False otherwise.
        """

        x = pycsp3.VarArray(size=len(self.ids), dom={int(v) for v in self.ids[:n_clusters]})

        for i, j in self.must_link:
            pycsp3.satisfy(x[i] == x[j])

        for i, j in self.cannot_link:
            pycsp3.satisfy(x[i] != x[j])

        return pycsp3.solve() is pycsp3.SAT
    
    def __add__(self, other):
        """
        Add two constraints objects.

        Parameters
        ----------
        other : ConstraintsObject
            The other constraints object to add.

        Returns
        -------
        ConstraintsObject
            The constraints object including the constraints of both operands.
        """

        if self.ids != other.ids:
            raise ValueError("The two constraints objects are defined on datasets of different sizes.")

        if not (self.X == other.X and self.y == other.y):
            raise Warning("The two constraints objects should be defined on the same dataset.")

        res = ConstraintsObject()

        res.must_link = self.must_link + other.must_link
        res.cannot_link = self.cannot_link + other.cannot_link

        if res.is_overconstrained():
            Warning("The problem is overconstrained.")

        return res