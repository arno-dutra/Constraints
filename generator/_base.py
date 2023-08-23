


class ConstraintsObject:

    def __init__(self):
        self.must_link = []
        self.cannot_link = []

    def add_must_link(self, i, j):
        self.must_link.append((i, j))

    def add_cannot_link(self, i, j):
        self.cannot_link.append((i, j))

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

        import pycsp3 as p3

        x = p3.VarArray(size=len(self.ids), dom=self.ids[:n_clusters])

        for i, j in self.must_link:
            p3.satisfy(x[i] == x[j])

        for i, j in self.cannot_link:
            p3.satisfy(x[i] != x[j])

        return p3.solve() is p3.SAT
    
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