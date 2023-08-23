from json import dumps


class ConstantSender(_BaseTag):

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
        >>> ConstantSender(path=args.constraints_manager_messenger_path, ...)
    y_pred: np.ndarray
        predicted labels
    """

    def __init__(self, 
        name="ConstantSender",
        path=None,
        variables={},
        ):

        if message is None:
            ValueError("You must provide the message given by argparse. Check the documentation for more information.")

        super().__init__(name, path)

        self.variables = variables

        self()

    def __call__(self):

        for var in self.msg["ask_for"]:
            self.send(var=self.variables[var])
