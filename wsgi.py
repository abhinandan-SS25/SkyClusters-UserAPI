import sys
project_home = '/home/abhinandansaha/SkyClusters-UserAPI'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from app import app as application