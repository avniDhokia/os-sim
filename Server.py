from flask import Flask, request
from flask_cors import CORS
from OperatingSystem import OperatingSystem
import json

app = Flask(__name__)
CORS(app)

os = OperatingSystem()


# data return structure
#   { cpu, scheduler, processes }
#
#   cpu:
#       current process
#
#   scheduler:
#       scheduler name
#       current state
#
#   processes:
#       each process: 
#

@app.route("/")
def hello_world():
    os.run()
    current_process = "Idle"
    if not os.cpu.current_process == None:
        current_process = json.loads('{"process":' + os.cpu.current_process.get_json_str() + '}')
        
        
    return {
        "cpu": {
            "current_process": current_process
        },
        "scheduler": {
            "name": os.scheduler.get_name(),
            "state": os.scheduler.get_json()
        }
    }

if __name__ == '__main__':
    app.run(debug=True)