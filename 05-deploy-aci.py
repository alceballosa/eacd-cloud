from azureml.core import Workspace
from azureml.core.environment import Environment
from azureml.core.model import InferenceConfig
from azureml.core.model import Model
from azureml.core.webservice import AciWebservice

ws = Workspace.from_config(path="./.azureml", _file_name="config.json")
model = Model(ws, name="xgboost_peptide_classifier", version=2)

env = Environment.from_conda_specification(
    name="cloud", file_path="./.azureml/cloud-env.yml"
)

inference_config = InferenceConfig(source_directory="./src", entry_script="score.py", environment=env)

deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

aci_service = Model.deploy(
    workspace=ws,
    name="peptide-classifier",
    models=[model],
    inference_config=inference_config,
    deployment_config=deployment_config,
)

aci_service.wait_for_deployment(show_output=True)
print(aci_service.state)
