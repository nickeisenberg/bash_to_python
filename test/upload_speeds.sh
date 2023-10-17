./copy_dir.sh \
  --source-dir /home/nicholas/Datasets/CelebA/img64_1000 \
  --save-dir s3://speed-demo-bucket/imgs \
  --profile nick \
  --notify-after 25

aws s3 cp /home/nicholas/Datasets/CelebA/img64_pq_1000 s3://speed-demo-bucket/imgs \
  --profile nick \
  --recursive
