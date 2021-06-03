from azureml.core import Workspace
from azureml.core.compute import AmlCompute
from azureml.core.compute import ComputeTarget
from azureml.core.compute_target import ComputeTargetException


ws = Workspace.from_config(path="./.azureml", _file_name="config.json")  # This automatically looks for a directory .azureml

# Choose a name for your CPU cluster
cpu_cluster_name = "cpu-clu-pep"

# Verify that the cluster does not exist already
try:
    cpu_cluster = ComputeTarget(workspace=ws, name=cpu_cluster_name)
    print("Found existing cluster, use it.")
except Exception:
    compute_config = AmlCompute.provisioning_configuration(
        vm_size="STANDARD_D2_V2",
        idle_seconds_before_scaledown=2400,
        min_nodes=0,
        max_nodes=2,
    )
    cpu_cluster = ComputeTarget.create(ws, cpu_cluster_name, compute_config)

cpu_cluster.wait_for_completion(show_output=True)
