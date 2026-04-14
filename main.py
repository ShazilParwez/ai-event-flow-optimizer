import subprocess
import os

port = os.environ.get("PORT", 8080)

subprocess.run([
    "streamlit",
    "run",
    "app.py",
    "--server.port=" + str(port),
    "--server.address=0.0.0.0",
    "--server.headless=true"
])