import os

#--------------------------------------------------
# Try to create a data loader that will recursively parse a data folder 
#--------------------------------------------------

class TreeImageFolder:

    def __init__(self, root, depth_limit):
        self.classes = []
        self.dataset = []
        self.get_all_classes(root, depth_limit)
        self.make_dataset(depth_limit)


    def get_all_classes(self, root, depth_limit=1):
    
        dirs = [d.name for d in os.scandir(root) if os.path.isdir(os.path.join(root, d.name))]
    
        for dir in dirs:
    
            target_dir = os.path.join(root, dir)
    
            innerdirs = [
                d.name for d in os.scandir(target_dir) if os.path.isdir(os.path.join(target_dir, d.name))
            ]
    
            if not innerdirs:
                if target_dir not in self.classes:
                    self.classes.append(target_dir)
            else:
                curdepth = len(target_dir.split('/')) - 1
                if curdepth == depth_limit:
                    self.classes.append(target_dir)
                    continue
                else:
                    self.get_all_classes(target_dir, depth_limit=depth_limit)
    
        return None


    def make_dataset(self, depth_limit):

        for classpath in self.classes:
            classname = "-".join(classpath.split("/")[-depth_limit:])

            for dirpath, dirname, fns in os.walk(classpath):

                for fn in fns:

                    if fn.endswith(".jpg"):
                       self.dataset.append(
                            (os.path.join(dirpath, fn), classname)
                        )

        return None


