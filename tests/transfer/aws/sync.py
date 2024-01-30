from shwrap.transfer.aws import sync
import os

home = os.environ["HOME"]
root = home + "/GitRepos/bash_to_python_project/bash_to_python/tests/transfer/aws/"

source_dir  = root + 'move/'
save_dir = "s3://sshtools-demo-bucket/"
profile = "nick"
logfile_location = root + "logfilename.log"

sync(
    source_dir, save_dir, profile, logfile_location
)
