from pyaws.pytorch_utils import TreeImageFolder
import os

HOME = os.environ['HOME']
root = f"{HOME}/GitRepos/pyaws_project/pyaws/_test/pytorch_utils/data"

dataset = TreeImageFolder(root=root, depth_limit=2)

print(dataset.fullpaths)

print(dataset.basepaths)

for inp in dataset.dataset:
    print(inp)
