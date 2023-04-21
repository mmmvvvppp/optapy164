This is an example of an overconstrained scheduling problem.  It uses a special problem fact (NullTool) instead of None to differentiate when it is impossible to arrive at a solution.  The xml solver file is not strictly required but is representative of a more complex use case.
It works fine in 8.23.0a0, but not in 8.28+

python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python main.py
