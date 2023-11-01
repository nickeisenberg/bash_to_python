from pyaws.pytorch_utils import TreeImageFolder

# this is buggy becuase of how I am taking care of depth. need to fix
root = "/home/nicholas/GitRepos/pyaws_project/pyaws/_test/pytorch_utils/data"

# this will work
root = "data"

dataset = TreeImageFolder(root=root, depth_limit=1)
for inp in dataset.dataset:
    print(inp)
