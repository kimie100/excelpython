# to run on local
python -m uvicorn api:app --reload



uvicorn api:app --reload

# to restart after git pull

sudo systemctl daemon-reload
sudo systemctl restart myfastapi
