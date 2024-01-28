This repo uses `subprocess` to call some common bash functions
from python. Currently only Darwin and Linux operating systems are supported.

# Installation
You can use `pip` to install the repo locally.
```bash
git clone https://github.com/nickeisenberg/bash_to_python.git
cd bash_to_python
pip install .
```

# Example

The following example is for sending with `scp`. The complete bash command that
this execute is:

```bash
scp -r -i <pem> -P <port> <source_path> <user>@<ip>:<save_path>`
```

With `btp`, the python setup would be:
```python
from btp.transfer import SecureCopyProtocol

scp = SecureCopyProtocol(
    user="<user>",
    ip="<ip>",
    port="<port>",
    pem="<pem>"
)


scp.send(
    source_path="<source_path>",
    save_path="<save_path>",
    with_tqdm=True,
    generate_logfile_to="<log_path>"
)
```

We can also use `btp.SecureCopyProtocol` to receive files from the remote
machine, ie the bash call:
```bash
scp -r -i <pem> -P <port> <user>@<ip>:<source_path> <save_path> `
```

The python setup for this would be 
```python
from btp.transfer import SecureCopyProtocol

scp = SecureCopyProtocol(
    user="<user>",
    ip="<ip>",
    port="<port>",
    pem="<pem>"
)


scp.receive(
    source_path="<source_path>",
    save_path="<save_path>",
    with_tqdm=True,
    generate_logfile_to="<log_path>"
)
```

# Notes
* The current wiki is completely out of data and needs to be updated.
* There is functionality in `btp.transfer.aws` that allows for sending and
  receiving to aws S3 buckets but there have been a bunch of changes since I
  have ast tested these tools.
