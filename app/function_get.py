import azure.functions as func
import json
import utilities

get_bp = func.Blueprint()

@get_bp.function_name(name="GetData")
@get_bp.route(route="api/get", auth_level=func.AuthLevel.ANONYMOUS)
def get_data(req: func.HttpRequest) -> func.HttpResponse:
    data = utilities.get_data()
    return func.HttpResponse(json.dumps(data, indent=4), status_code=200)
