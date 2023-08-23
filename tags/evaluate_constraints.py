from json import dumps


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
        >>> EvaluateConstraints(message=args.constraints_manager_messenger_path, ...)
    y_pred: np.ndarray
        predicted labels
    """

    def __init__(self, 
        name="EvaluateConstraints",
        path=None,
        
        ):

        if message is None:
            ValueError("You must provide the message given by argparse. Check the documentation for more information.")

        super().__init__(name, path)

        self()

    def __call__(self):

        for point in self.msg["points_to_predict_class"]:
            self.send(point=point, y_pred=y_pred[points])
