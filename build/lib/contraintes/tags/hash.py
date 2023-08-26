from json import dumps
from contraintes.tags._base import _BaseTag


class HashTag(_BaseTag):

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
    variables: dict
        variables to send
    """

    def __init__(self, 
        name="HashTag",
        path=None,
        ):
        
        if path is None:
            ValueError("You must provide the path given by argparse. Check the documentation for more information.")

        super().__init__(name, path)


    def __call__(self):
        
        self.hash = self.msg["hash"]
        return self.hash