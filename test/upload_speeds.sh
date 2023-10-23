./copy_dir_speed.sh \
  --source-dir /home/nicholas/Datasets/CelebA/batched \
  --save-dir s3://speed-demo-bucket/imgs \
  --profile nick \
  --notify-after 1

./copy_dir.sh \
  --source-dir /home/nicholas/Datasets/CelebA/batched \
  --save-dir s3://speed-demo-bucket/imgs \
  --profile nick \
  --notify-after 1

./awscp.sh \
  --source-dir /home/nicholas/Datasets/CelebA/batched \
  --save-dir s3://speed-demo-bucket/imgs \
  --profile nick

aws s3 cp /home/nicholas/Datasets/CelebA/batched s3://speed-demo-bucket/imgs \
  --profile nick \
  --recursive

aws s3 sync /home/nicholas/Datasets/CelebA/batched s3://speed-demo-bucket/imgs \
  --profile nick
