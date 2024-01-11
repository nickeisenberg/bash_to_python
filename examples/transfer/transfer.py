from sshtools.transfer import SecureCopyProtocol

scp = SecureCopyProtocol(
    user="nick",
    ip="54.183.226.197",
    port="22"
)

scp.scp(
    source_path="",
    save_path="/ebs0/nick/Tmp/sshtools_test",
)
