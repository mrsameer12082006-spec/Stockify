"""Root Streamlit entrypoint.

Keeps `streamlit run app.py` working by executing `frontend/app.py` as a script
on every rerun.
"""

from pathlib import Path
import runpy


FRONTEND_APP = Path(__file__).resolve().parent / "frontend" / "app.py"
runpy.run_path(str(FRONTEND_APP), run_name="__main__")
