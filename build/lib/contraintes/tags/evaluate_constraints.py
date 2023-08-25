from json import dumps
from contraintes.tags._base import _BaseTag


class EvaluateConstraints(_BaseTag):

    """
    Evaluate the constraints given by the constraints manager.
    
    Parameters
    ----------
    name: str
        name of the tag
    path: str
        path where instructions for tags are given
        >>> parser.add_argument("-cmm", "--constraints-manager-messenger-path", type=str, default="", help="Should not be used manually. Used by the constraints manager to send datas to the pipeline.")
        >>> args = parser.parse_args()
        >>> ...
        >>> EvaluateConstraints(path=args.constraints_manager_messenger_path, ...)
    y_pred: np.ndarray
        predicted labels
    """

    def __init__(self, 
        name="EvaluateConstraints",
        path=None,
        y_pred=None,
        ):

        if path is None:
            ValueError("You must provide the path given by argparse. Check the documentation for more information.")

        super().__init__(name, path)

        self(y_pred=y_pred)

    def __call__(self, y_pred=None):

        for point in self.msg["points_to_predict_class"]:
            self.send(point=point, y_pred=y_pred[point])
