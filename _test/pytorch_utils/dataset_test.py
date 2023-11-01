from pyaws.pytorch_utils import TreeImageFolder
import os


HOME = os.environ['HOME']

# this is buggy becuase of how I am taking care of depth. need to fix
root = f"{HOME}/GitRepos/pyaws_project/pyaws/_test/pytorch_utils/data"

# this will work
root = "data"

dataset = TreeImageFolder(root=root, depth_limit=1)


for inp in dataset.dataset:
    print(inp)

os.path.basename(inp[0])

os.path.basename("data")
