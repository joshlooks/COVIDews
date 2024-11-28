import os
import sys

num = sys.argv[1]
identity = sys.argv[2]
scripts_dir = os.path.dirname(__file__)
results_dir = os.path.join(scripts_dir,identity)
i = 0
fpath = os.path.join(results_dir,f'{num}_{i}.npy')
print(fpath)