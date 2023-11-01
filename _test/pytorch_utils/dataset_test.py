from pyaws.pytorch_utils import TreeImageFolder

root = "data"
dataset = TreeImageFolder(root=root, depth_limit=1)
for inp in dataset.dataset:
    print(inp)
