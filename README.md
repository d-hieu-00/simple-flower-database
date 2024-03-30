# Datasets
Here: https://www.robots.ox.ac.uk/%7Evgg/data/flowers/102/

# Python dependencies
- torch
- clip
- psycopg2

# Setup
- Re-Run `model/setup_v1.ipynb` to get:
    - dataset
    - pre-trained model
    - create database form dataset
    - [use trained model CLIP](https://github.com/openai/CLIP)
**Note**: Can model what model/ dataset you want from internet. You need modify `server/handler/model_handler_v1.py`
to load and run the model you want.

# Build Frontend
- Use Vuejs to build a simple web app
```
cd web
npm i
npm run build
```

# Run http.server
- Config of Backend store in `server/config.py`
```
cd server
python main.py
```
