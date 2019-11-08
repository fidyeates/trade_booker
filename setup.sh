#!/bin/bash
set -euo pipefail

if [ -z "${TRADE_BOOKER_PATH:-}" ]; then
  TRADE_BOOKER_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
fi

# Setup Python Dependancies
pip3 install -r $TRADE_BOOKER_PATH/requirements.txt

export PYTHONPATH=${PYTHONPATH:-}:$TRADE_BOOKER_PATH

python3 $TRADE_BOOKER_PATH/bin/setup.py
python3 $TRADE_BOOKER_PATH/bin/app.py &
TRADE_BOOKER_PID=$!
echo "webserver running on port: 8888 with pid: $TRADE_BOOKER_PID"
