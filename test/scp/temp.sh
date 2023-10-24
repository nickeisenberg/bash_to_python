port = "2222"
source_path = "/home/ubuntu/pyscripts/scp/tempfile.txt"
save_path = "/home/nicholas/"
user = "nicholas"
ip = "174.72.155.21"
path_to_bash = "/home/ubuntu/pyscripts/scp/scp.sh"

./scp.sh \
  --port 2222 \
  --source-path /home/ubuntu/pyscripts/scp/share \
  --save-path /home/nicholas/ \
  --user nicholas \
  --ip 174.72.155.21

#--------------------------------------------------

port = "22"
source_path = "/home/nicholas/GitRepos/pyaws/test/scp/move"
save_path = "/home/ubuntu/movedir"
user = "ubuntu"
ip = "50.18.80.35"
path_to_bash = "/home/nicholas/GitRepos/pyaws/transfer/scripts/scp.sh"

./scp.sh \
  --port 22 \
  --source-path /home/nicholas/GitRepos/pyaws/test/scp/move \
  --save-path /home/ubuntu/movedir \
  --user ubuntu \
  --ip 50.18.80.35

#--------------------------------------------------

./awscp.sh \
  --source-dir /home/nicholas/Datasets/CelebA/batched \
  --save-dir s3://speed-demo-bucket/imgs \
  --profile nick
