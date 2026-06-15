#!/bin/bash
# NayePankh Analytics Runner
# Activates venv and runs the analytics pipeline

REPO_DIR="/Users/dharika/Desktop/nayepankh-data-analytics"
cd "$REPO_DIR"
source "$REPO_DIR/venv/bin/activate"
python "$REPO_DIR/src/nayepankh_analytics.py"
