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
