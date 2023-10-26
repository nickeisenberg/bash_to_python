"""
This does not rely on pyaws. It is very slow and the pyaws method is much faster.

This requires requires the follwing setup to work

1. First ssh into the ec2 instance and open up `/etc/ssh/ssh_config` and 
uncomment the line that says `ForwardX11 no` and replace `no` with `yes`.
Save the file. Note that this file must be editted with `sudo vi` as this
is a proftected file.

2. Stop the connection and reboot the ec2 instance with the line:
    ```
    aws ec2 reboot-instances \
            --region <region_name> \
            --instance-ids <instance_id> \
            --profile <profile_name>
    ```

3. Now, ssh back in the instance with `ssh -X -i <key-pair.pem> ubuntu@<ip-addr>`

4. Make sure `tkinter` is installed. Do this with `sudo apt install python3-tk`
"""

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

plt.figure()

plt.plot([1, 2, 3], [1, 2, 3])

plt.show()
