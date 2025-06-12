read -p "Key file path: " "file_loc"
ssh -i "$file_loc" ec2-user@35.176.210.16 << 'EOF'
  sudo yum -y install python3 python3-pip
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r ./dashboard/requirements.txt
  nohup streamlit run ./dashboard/Home.py &
  exit
EOF