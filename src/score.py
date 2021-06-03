import json
import os
import pickle

import joblib
import numpy as np

import feature
import pepfilter

ACCEPTED_AAs = set([
    "A",
    "R",
    "N",
    "D",
    "C",
    "Q",
    "E",
    "G",
    "H",
    "I",
    "L",
    "K",
    "M",
    "F",
    "P",
    "S",
    "T",
    "W",
    "Y",
    "V",
])


def init():
    global model
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It's the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION).
    # For multiple models, it points to the folder containing all deployed models (./azureml-models).
    model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "xgboost_peptide_classifier.pkl"
    )
    model = joblib.load(model_path)


def run(raw_data):
    data = list(json.loads(raw_data)["data"])
    results = []

    for seq in data:
        is_valid = pepfilter.amp_filter(seq, ACCEPTED_AAs, 6, 35, 2)
        if is_valid:
            try:
                feats = list(feature.get_features(seq).values())[1:]
                y_hat = model.predict(np.array([feats]))[0]
                if y_hat == 0:
                    results.append(seq + ": Péptido no-antimicrobiano.")
                else:
                    results.append(seq + ": Péptido antimicrobiano.")
            except:
                results.append(
                    seq + ": Péptido generó error en extracción de características."
                )
        else:
            results.append(seq + ": Péptido no cumple los parámetros para procesar.")

    # Make prediction.
    # You can return any data type as long as it's JSON-serializable.
    return results
