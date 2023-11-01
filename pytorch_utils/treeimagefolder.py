import os

#--------------------------------------------------
# Try to create a data loader that will recursively parse a data folder 
#--------------------------------------------------

class TreeImageFolder:

    def __init__(self, root, depth_limit):
        self.classes = []
        self.dataset = []
        self.depth_corrector = self.split_path(root)
        self.get_all_classes(root, depth_limit)
        self.make_dataset(depth_limit)


    def get_all_classes(self, root, depth_limit=1):
    
        dirs = [
            d.name for d in os.scandir(root) 
            if os.path.isdir(os.path.join(root, d.name))
        ]

        for dir in dirs:

            target_dir = os.path.join(root, dir)

            innerdirs = [
                d.name for d in os.scandir(target_dir) 
                if os.path.isdir(os.path.join(target_dir, d.name))
            ]

            if not innerdirs:
                if target_dir not in self.classes:
                    self.classes.append(target_dir)
            else:
                # curdepth = len(target_dir.split('/')) - 1
                curdepth = self.split_path(target_dir) - self.depth_corrector
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

    
    @staticmethod
    def split_path(path):
        # Initialize an empty list to store path components
        parts = []
        
        # Keep splitting the path until no more directories are left
        while True:
            path, folder = os.path.split(path)
            if folder:
                # Append the folder to the start of the parts list
                parts.insert(0, folder)
            else:
                if path:
                    # Append the drive (if any) to the start of the parts list
                    parts.insert(0, path)
                break
    
        return len(parts)


