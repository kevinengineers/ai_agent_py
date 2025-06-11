from functions.get_files_info import get_files_info

print(get_files_info("calculator", "."))
print(get_files_info("calculator", "pkg"))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))

import os
print(f"Current directory: {os.getcwd()}")
print(f"Calculator absolute path: {os.path.abspath('calculator')}")
print(f"Dot absolute path: {os.path.abspath('.')}")
