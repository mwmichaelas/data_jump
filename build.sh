python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install requests
pip install pip-tools pip-chill
pip-compile requirements.in
pip-sync
