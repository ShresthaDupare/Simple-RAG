"""
Study RAG — Streamlit entry point.

For local development:
    streamlit run app.py

For Streamlit Community Cloud:
    Set the entry point to: src/ui/app.py
"""

import sys
from pathlib import Path

# Add project root to path
_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# Run the real app
exec(open(_root / "src" / "ui" / "app.py", encoding="utf-8").read())
