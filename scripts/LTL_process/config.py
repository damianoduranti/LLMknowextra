import os

current_script_directory = os.path.dirname(os.path.abspath(__file__))
repo_root_directory = os.path.dirname(os.path.dirname(current_script_directory))
LTLFUCBIN = os.path.join(repo_root_directory, "nuXmv", "bin", "nuXmv")

MAX_VIRTUAL_MEMORY = 4 * 1024 * 1024 * 1024 # 4 GB