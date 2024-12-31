import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import json
import logging
import utilities

schedule_bp = func.Blueprint()

@schedule_bp.function_name(name="ManageVM")
@schedule_bp.route(route="api/vm", auth_level=func.AuthLevel.ANONYMOUS)
def manage_vm(req: func.HttpRequest) -> func.HttpResponse:
    vmData = json.loads(req.get_body())
    subscriptionId = vmData["id"].split("/")[2]
    resourceGroup = vmData["id"].split("/")[4]
    vmName = vmData["id"].split("/")[8]

    compute_client = ComputeManagementClient(
        credential=DefaultAzureCredential(exclude_environment_credential=True), subscription_id=subscriptionId
    )

    if req.method == "POST":
        logging.info("STARTING VM")
        start_vm_event = compute_client.virtual_machines.begin_start(
            resource_group_name=resourceGroup, vm_name=vmName
        )
        start_vm_event.wait()
    elif req.method == "DELETE":
        logging.info("STOPPING VM")
        stop_vm_event = compute_client.virtual_machines.begin_deallocate(
            resource_group_name=resourceGroup, vm_name=vmName
        )
        stop_vm_event.wait()
    else:
        return func.HttpResponse("Method not allowed", status_code=405)

    return func.HttpResponse("OK")
