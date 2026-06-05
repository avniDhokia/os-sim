from flask import Flask, request, jsonify
from flask_cors import CORS
from OperatingSystem import OperatingSystem
import json

app = Flask(__name__)
CORS(app)


os = OperatingSystem()

# process request to create a new process
@app.route("/addProcess", methods=['POST'])
def add_process():
    # get name from post
    os.add_process(request.get_json()['name'])

    return jsonify({"status":"ok", "created": True}), 201


# process request to kill a process
@app.route("/killProcess", methods=['POST'])
def kill_process():
    valid = os.remove_process_id( (request.get_json()['id']) )
    
    if valid:
        return jsonify({"status":"ok", "created": True}), 201
    
    return jsonify({"status":"error","message":"Process not found"}), 400


# request to change scheduler
@app.route("/changeScheduler", methods=['POST'])
def change_scheduler():
    new_scheduler = request.get_json()['scheduler']
    valid = os.change_scheduler(new_scheduler)

    return jsonify({"status":"ok", "created": True}), 201


# boost processes to q0
@app.route("/boostProcesses", methods=['POST'])
def boost_processes():
    os.scheduler.boost()
    return jsonify({"status":"ok", "created": True}), 201

#
#   response structure (json):
#
#   cpu
#       current_process
#       events
#           [switch?]
#   os
#       blocked_processes
#       scheduler
#           name
#           state
#               processes
#           events
#               [boost?,new_process?]
#

@app.route("/")
def hello_world():
    os.run()
    current_process = "Idle"
    if not os.cpu.current_process == None:
        current_process = json.loads('{"process":' + os.cpu.current_process.get_json_str() + '}')
        

    return {
        "cpu": {
            "current_process": current_process,
            "events": os.cpu.get_tick_events()
        },
        "os":{
            "blocked_processes": os.get_blocked_processes_json(),
            "scheduler": {
                "name": os.scheduler.get_name(),
                "state": os.scheduler.get_json(),
                "events": os.scheduler.get_tick_events()
            }
        }


    }

if __name__ == '__main__':
    app.run(debug=True)