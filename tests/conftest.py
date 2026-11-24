import os
import sys

# Add src directory to Python path so that pytest can import src.app
src_path = os.path.join(os.path.dirname(__file__), "..", "src")
sys.path.insert(0, os.path.abspath(src_path))
