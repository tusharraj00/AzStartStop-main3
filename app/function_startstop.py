import azure.functions as func
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import DefaultAzureCredential
import datetime
import logging
import pytz
import utilities

startstop_bp = func.Blueprint()

@startstop_bp.function_name(name="StartStop")
@startstop_bp.schedule(
    schedule="*/5 * * * *", arg_name="timer", run_on_startup=False, use_monitor=False
)
def start_stop_vms(timer):
    current_timezone = utilities.get_setting("Timezone")
    if not current_timezone:
        current_timezone = "UTC"
    
    current_time = datetime.datetime.now(pytz.timezone(current_timezone))
    logging.info(f"Evaluating stop at {current_time}")

    for subscription in utilities.get_subscriptions():
        logging.info(f"Processing subscription: {subscription['id']}")
        compute_client = ComputeManagementClient(
            credential=DefaultAzureCredential(exclude_environment_credential=True), subscription_id=subscription["id"]
        )

        events = []
        for vm in compute_client.virtual_machines.list_all():
            logging.info(vm.id)
            vm_state = utilities.extract_vm_state(vm, compute_client)
            logging.info(f"[{vm.name}]: {vm_state}")

            if vm_state == "running":
                utilities.log_vm_event(vm, "stopping")
                events.append(utilities.set_vm_state('stopped', vm, compute_client))
                logging.info(f"[{vm.name}]: stopping...")

        for event in events:
            event.wait()