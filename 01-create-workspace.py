import json

from azureml.core import Workspace
from azureml.core.authentication import InteractiveLoginAuthentication

option = int(input("Type 1 to create the workspace, type 0 to re-use it."))
with open("secret.json") as f:
    secret = json.load(f)

tenant_id = secret["tenant_id"]


interactive_auth = InteractiveLoginAuthentication(tenant_id=secret["tenant_id"])

if option == 1:
    # az cli https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-how-to-find-tenant
    ws = Workspace.create(
        name="azure-ml",
        subscription_id=secret["subscription_id"],  # Se encuentra en subscripciones
        resource_group="rg-cloud-course",
        create_resource_group=False,
        location="eastus2",
        auth=interactive_auth,
    )
else:
    ws = Workspace.get(
        name="azure-ml",
        subscription_id=secret["subscription_id"],
        resource_group="rg-cloud-course",
        auth=interactive_auth,
    )


# write out the workspace details to a configuration file: .azureml/config.json
ws.write_config(path=".azureml")
