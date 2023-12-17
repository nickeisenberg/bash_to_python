"""
An example template of pyaws.transfer.cp_recursive()

An example of an acceptable s3 bucket path is s3://speed-demo-bucket/imgs
"""

from sshtools.transfer.aws import sync

source_dir = "/path/to/data/to/be/moved"
save_dir = "/path/to/where/data/will/be/moved/to"
profile = "<aws profile name>"
logfile_location = "/local/path/to/save/logfile/logfilename.log"

sync(
    source_dir, save_dir, profile, logfile_location
)

