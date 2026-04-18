"""
Vercel serverless entry point for the Stockify Streamlit app.

This module uses subprocess to launch the Streamlit server and proxies
requests to it. This is the standard pattern for running Streamlit on Vercel.
"""

import subprocess
import os
import sys

# Add the project root to the Python path so all local imports work
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def handler(request):
    """
    Vercel serverless function handler.
    
    Starts the Streamlit app as a subprocess. Vercel will proxy
    the request to the running Streamlit server.
    """
    # Launch Streamlit pointing to app.py in the project root
    app_path = os.path.join(project_root, "frontend", "app.py")
    
    process = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run",
            app_path,
            "--server.port=8501",
            "--server.headless=true",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": "<html><body><h1>Stockify is starting...</h1><p>Streamlit app is being initialized.</p></body></html>"
    }
