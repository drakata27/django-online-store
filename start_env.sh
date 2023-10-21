#!/bin/bash

os=$1

if [ "$os" = "wsl" ]; then
    echo "Activating venv for WSL"
    source venv/Scripts/activate
elif [ "$os" = "mac" ]; then
    echo "Activating venv for macOS"
    source venv/bin/activate
else
    echo "Invalid input"
    exit 1
fi

echo "Starting the server..."
python3 manage.py runserver

