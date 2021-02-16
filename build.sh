python -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install requests
pip install pytest
pip install pip-tools pip-chill
pip-compile requirements.in
pip-sync
