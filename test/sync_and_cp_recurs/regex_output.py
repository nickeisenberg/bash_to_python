import re

string = "Completed 65.0 MiB/65.9 MiB (4.4 MiB/s) with 5 file(s) remaining"

l = string.split(" ")[:6]

"PROGRESS " + str.join(" ", l[1:4]) + "    SPEED " + str.join(" ", l[4:])

