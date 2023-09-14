from json import dumps
from contraintes.tags._base import _BaseTag


class EvaluateRepresentation(_BaseTag):

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
        name="EvaluateRepresentation",
        path=None,
        imatag=False,
        ):

        if imatag:
            if path is None:
                ValueError("You must provide the path given by argparse. Check the documentation for more information.")

            super().__init__(name, path)


    # def __call__(self, y_pred=None):

    #     for point in self.msg["points_to_predict_class"]:
    #         self.send(point=point, y_pred=y_pred[point])

    def __call__(self, encoded_train=None, encoded_test=None, x_test_pred=None, x_test=None, train_labels=None, test_labels=None, dataset: str= None, model: str = None, encodeur_name="TimeMAEEncoder", args: dict = {}, hyperparameters_hash: str = None, epoch: int = ""):

        import pandas as pd
        import numpy as np
        from sklearn import metrics
        from sklearn.cluster import KMeans
        import os


        mesures = {}

        mesures["Model"] = model
        mesures["args"] = args
        # Compute hash to make an id for this set of hyperparameters
        mesures["hash"] = hyperparameters_hash
        model_file_name = f"__encoder_{encodeur_name}_{dataset}_%(hash)s_epoch%(e)s.h5" % {"hash": str(hyperparameters_hash), "e": epoch}
        mesures["model_file_name"] = model_file_name

        # datasets = list_available_tsc_datasets()
        metrics_reconstruction = [metrics.explained_variance_score, metrics.mean_absolute_error, metrics.mean_squared_error]
        metrics_X_predlabels = [metrics.silhouette_score, metrics.calinski_harabasz_score, metrics.davies_bouldin_score, ]
        metrics_labels_predlabels = [metrics.adjusted_mutual_info_score, metrics.adjusted_rand_score, metrics.completeness_score, metrics.fowlkes_mallows_score, metrics.homogeneity_score, metrics.mutual_info_score, metrics.normalized_mutual_info_score, metrics.rand_score, metrics.v_measure_score]
        path = "./local/__resultats_%(m)s.csv" % {"m": model}

        mesures["Dataset"] = dataset
        mesures["Epoch"] = epoch

        # Evaluate reconstruction
        if x_test_pred is not None and x_test is not None:
            print("Evaluating reconstruction")
            for metric in metrics_reconstruction:
                
                try:
                    mesures[metric.__name__] = metric(x_test.reshape(x_test.shape[0], -1), x_test_pred.reshape(x_test_pred.shape[0], -1))
                except:
                    mesures[metric.__name__] = np.nan

        # Clustering
        print("Clustering")
        n_classes = len(np.unique(train_labels))

        clusterer = KMeans(n_clusters=n_classes, **args.clustering_hyperparameters)
        clusterer.fit(encoded_train)

        for dataset_type, encoded_dataset, gold_labels in [("train", encoded_train, train_labels), ("test", encoded_test, test_labels)]:
            predicted_labels = clusterer.predict(encoded_dataset)

            # Evaluate clustering
            print("Evaluating clustering on", dataset_type)
            for metric in metrics_X_predlabels:
                
                try:
                    mesures[f"%(d)s_%(m)s" % {"d": dataset_type, "m": metric.__name__}] = metric(encoded_dataset, predicted_labels)
                except:
                    mesures[f"%(d)s_%(m)s" % {"d": dataset_type, "m": metric.__name__}] = np.nan

            for metric in metrics_labels_predlabels:

                try:
                    mesures[f"%(d)s_%(m)s" % {"d": dataset_type, "m": metric.__name__}] = metric(gold_labels, predicted_labels)
                except:
                    mesures[f"%(d)s_%(m)s" % {"d": dataset_type, "m": metric.__name__}] = np.nan


        # Store results into a csv 
        print("Storing results")
        df_dictionary = pd.DataFrame([mesures])
        import os.path
        if os.path.isfile(path):
            results = pd.read_csv(path, sep=",", index_col=None)
            results = pd.concat([results, df_dictionary])
        else:
            results = df_dictionary
        results.to_csv(path, sep=",", index=False)
