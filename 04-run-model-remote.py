# 06-run-pytorch-data.py
from azureml.core import Dataset
from azureml.core import Environment
from azureml.core import Experiment
from azureml.core import ScriptRunConfig
from azureml.core import Workspace

if __name__ == "__main__":
    ws = Workspace.from_config(path="./.azureml", _file_name="config.json")
    datastore = ws.get_default_datastore()
    dataset = Dataset.File.from_files(path=(datastore, "datasets/peptides"))

    experiment = Experiment(
        workspace=ws, name="day1-experiment-train-peptides-remote"
    )

    config = ScriptRunConfig(
        source_directory="./src",
        script="train-remote.py",
        compute_target="cpu-clu-pep",
        arguments=[
            "--data_path",
            dataset.as_named_input("pep_dataset").as_mount(),
            "--learning_rate",
            0.001,
            "--n_estimators",
            750,
            "--reg_alpha",
            0.5,
        ],
    )
    # set up pytorch environment
    env = Environment.from_conda_specification(
        name="cloud", file_path="./.azureml/cloud-env.yml"
    )
    config.run_config.environment = env

    run = experiment.submit(config)
    aml_url = run.get_portal_url()
    print("Submitted to compute cluster. Click link below")
    print("")
    print(aml_url)
    # Register model from run id
    run.wait_for_completion(show_output=True)
    model = run.register_model(
        model_name="xgboost_peptide_classifier",
        tags={"area": "biology"},
        model_path="outputs/xgboost_peptide_classifier.pkl",
    )
