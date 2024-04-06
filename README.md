This repo uses `subprocess` to call some common bash functions
from python. There are also some 100% python implemented functions that are
bash adjacent. Currently only Darwin and Linux operating systems are supported.

# Installation
You can use `pip` to install the repo locally.
```bash
git clone https://github.com/nickeisenberg/shwrap.git
cd shwrap
pip install .
```

# Example

The following example is for sending with `scp`. The complete bash command that
this execute is:

```bash
scp -r -i <pem> -P <port> <source_path> <user>@<ip>:<save_path>`
```

With `shwrap`, the python setup would be:
```python
from shwrap.transfer import SecureCopyProtocol

scp = SecureCopyProtocol(
    user="<user>",
    ip="<ip>",
    port="<port>",
    pem="<pem>"
)


scp.put(
    source_path="<source_path>",
    save_path="<save_path>",
    with_tqdm=True,
    generate_logfile_to="<log_path>"
)
```

We can also use `shwrap.SecureCopyProtocol` to receive files from the remote
machine, ie the bash call:
```bash
scp -r -i <pem> -P <port> <user>@<ip>:<source_path> <save_path> `
```

The python setup for this would be 
```python
from shwrap.transfer import SecureCopyProtocol

scp = SecureCopyProtocol(
    user="<user>",
    ip="<ip>",
    port="<port>",
    pem="<pem>"
)


scp.get(
    source_path="<source_path>",
    save_path="<save_path>",
    with_tqdm=True,
    generate_logfile_to="<log_path>"
)
```

# Notes
* The current wiki is completely out of data and needs to be updated. 
* There is functionality in `shwrap.transfer.aws` that allows for sending and
  receiving to aws S3 buckets. These tools have only been tested on Linux. They
  probably would work on Mac but I have not tested.
