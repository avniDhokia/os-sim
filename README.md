
# os-sim

## dependencies
- colorama
- flask
- flask_cors


## how to run

there are 2 ways to run:
- terminal-only version
- web version

## terminal-only version

1. on a terminal, run:
    `source venv/bin/activate`  to activate venv (create venv if not already created)

2. run:
    `python3 test_os.py`         to run the sim 

### web version

1. [on terminal 1] run:
    `source venv/bin/activate`  to activate venv (create venv if not already created)
    `python3 Server.py`         to run server

2. [on terminal 2] in the folder frontend/client/src run:
    `npm run dev`               to run client

3. in a browser, visit the localhost link provided in terminal 2