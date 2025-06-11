read -p "Key file path: " "file_loc"
scp -i $file_loc Home.py data.py report.py charts.py subscription.py .env requirements.txt ec2-user@35.176.210.16:./dashboard
scp -i $file_loc -r pages/ ec2-user@35.176.210.16:./dashboard