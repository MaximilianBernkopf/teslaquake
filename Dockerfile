FROM python:3.10-bullseye

EXPOSE 8501

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY teslaquake .

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]