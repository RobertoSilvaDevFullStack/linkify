import sys
import os

print("Python executable:", sys.executable)
print("Current working directory:", os.getcwd())
print("Python version:", sys.version)
print("Files in current directory:")
for f in os.listdir("."):
    print(f"  {f}")
