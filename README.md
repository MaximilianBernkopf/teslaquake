# Teslaquake

Coding Challenge for Tesla applictation.

```
conda create -n teslaquake python=3.10 pandas numpy fastapi psycopg2 plotly sqlalchemy scipy
conda activate teslaquake
pip install streamlit
pip install sqlmodels

set -a &&. .env && set +a && streamlit run teslaquake/app.py
```


```
. .env && docker build -t streamlit .
docker run -p $PORT:$PORT --env-file .env streamlit
```

TODO:
- Fix dependencies to specific version
- Fix docker railway port madness
- Export conda env