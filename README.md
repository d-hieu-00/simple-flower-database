# Datasets
Here: https://www.robots.ox.ac.uk/%7Evgg/data/flowers/102/

# Python dependencies
- transformers
- nltk

# Setup
- Re-Run `model/setup.ipynb` to get:
    - dataset
    - pre-trained model
    - create database form dataset
    - save pre-trained model to local
**Note**: Can model what model/ dataset you want from internet. You need modify `server/handler/model_handler.py`
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
