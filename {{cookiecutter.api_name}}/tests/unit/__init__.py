import os
import sys

"""sets up the python path to source the api code so the interpretor knows to load it as modules"""
root_app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.abspath(os.path.join(root_app_dir, ".")))
