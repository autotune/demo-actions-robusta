from robusta.api import *

# see: https://docs.robusta.dev/master/developer-guide/actions/triggers-and-events.html#events-and-triggers
@action
def report_scheduling_failure(event: ReplicaSetEvent): # We use ReplicaSetEvent to get the event object.
    actual_event = event.get_event()

    print(f"This print will be shown in the robusta logs={actual_event}")

    if actual_event.type.casefold() == f'Normal'.casefold() and 
        # actual_event.reason.casefold() == f'ScalingReplicaSet'.casefold():
        _report_succeded_scheduling(event, actual_event.involvedObject.name, actual_event.message)

def _report_succeded_scheduling(event: EventEvent, pod_name: str, message: str):
    custom_message = ""
    # if "affinity/selector" in message:
    #     custom_message = "Your pod has a node 'selector' configured, which means it can't just run on any node. For more info, see: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector"

    # this is how you send data to slack or other destinations

    # Note - is it sometimes better to create a Finding object instead of calling event.add_enrichment, but this is out of the scope of this tutorial

    event.add_enrichment([
        MarkdownBlock(f"Succeeded to schedule a pod named '{pod_name}'!\nerror: {message}\n\n{custom_message}"),
    ])
