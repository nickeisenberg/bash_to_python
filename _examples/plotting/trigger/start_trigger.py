"""
Use this script to set the local folder that will receive all incoming 
png images and auto-open them.
"""

from pyaws.plotting import start_trigger

path_to_image_folder = "/path/to/local/folder/to/actvate/the/trigger"

start_trigger(path_to_image_folder)
