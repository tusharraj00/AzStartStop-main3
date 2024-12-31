import azure.functions as func
from .function_startstop import startstop_bp
from .function_schedule import schedule_bp
from .function_get import get_bp

app = func.FunctionApp()

app.register_blueprint(startstop_bp)
app.register_blueprint(schedule_bp)
app.register_blueprint(get_bp)
