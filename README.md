# to run on local

uvicorn api:app --reload

# to restart after git pull

sudo systemctl daemon-reload
sudo systemctl restart myfastapi
