FROM python:3.10-bullseye

EXPOSE $PORT

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY teslaquake .

#ENV STREAMLIT_SERVER_PORT=$PORT
#ENTRYPOINT ["streamlit", "run", "app.py"]

CMD ["sh", "-c", "streamlit run --server.port $PORT app.py"] 
