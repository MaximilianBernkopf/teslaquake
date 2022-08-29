# Teslaquake

Coding Challenge for Tesla applictation.

```
conda create -n teslaquake python=3.10 pandas numpy fastapi
conda activate teslaquake
pip install streamlit
pip install sqlmodels
streamlit run teslaquake/app.py
```


```
docker build -t streamlit .
docker run -p 8501:8501 --env-file .env streamlit
```

TODO:
- Fix dependencies to specific version