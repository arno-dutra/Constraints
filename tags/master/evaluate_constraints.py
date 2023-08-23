from contraintes.tags.master._base_master import _BaseMaster


class EvaluateConstraints(_BaseMaster):
    """
    Tag master
    """
    def __init__(self, path, constraints, name="EvaluateConstraints"):
        super().__init__(name, path)

        self.constraints = constraints

    def prepare_message(self):
        
        datas = {}

        datas["points_to_predict_class"] = self.constraints.get_points()

        return self.name, datas

    def score(self):
        """
        compute the score of the model in relation to the constraints
        """
        
        if self.answer is None:
            self.read_answer()

        clustering = {}
        for d in self.answer:
            if "points" in d and "y_pred" in d":
                points = d["points"]
                y_pred = d["y_pred"]
                clustering[points] = y_pred
        results = self.constraints.is_respected(clustering, method="count")

        return results