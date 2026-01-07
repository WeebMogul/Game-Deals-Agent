#!/bin/bash 

echo "Starting ADK API server on port 8000..."
adk api_server --port 8000 --host 0.0.0.0 & 

sleep 3

echo "Starting Streamlit app on port 8501..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

wait