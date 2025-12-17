"""
Streamlit app entry point for Streamlit Cloud deployment
This file is at the root level so Streamlit Cloud can find it automatically
"""

import subprocess
import sys
import os

# Make sure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import the app
import app
