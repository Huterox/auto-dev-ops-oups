#!/usr/bin/env bash

function get_python3() {
    if command -v python3 &> /dev/null
    then
        echo "python3"
    else
        echo "Python3 not found. Please install Python3.7 or higher."
        exit 1
    fi
}

PYTHON_CMD=$(get_python3)

if $PYTHON_CMD -c "import sys; sys.exit(sys.version_info < (3, 7))"; then
    echo Installing missing packages...
    $PYTHON_CMD -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
else
    echo "Python 3.7 or higher is required to run App."
    exit 1
fi

# run the command below to start the app
streamlit run /app/main.py --port=8080


