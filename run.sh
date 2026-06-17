#!/bin/bash

python -m streamlit run app.py \
--server.port 8501 \
--server.headless true \
--server.enableCORS false \
--server.enableXsrfProtection false \
--server.fileWatcherType none
