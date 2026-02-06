# scripts/run_report.py
import sys
import os

# Add project root directory to path
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

# Import dashboard module (this will execute the dashboard generation)
import reporting.scripts.dashboard
