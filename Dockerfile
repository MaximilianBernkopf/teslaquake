FROM python:3.10-bullseye

EXPOSE $PORT

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN mkdir ~/.streamlit
COPY config.toml ~/.streamlit/config.toml

COPY teslaquake .

#TODO: 
#THIS SHOULD WORK, BUT FOR WHATEVER REASON IT DOESNT... ¯\_(ツ)_/¯
#INSTEAD THIS MADNESS....
#ENV STREAMLIT_SERVER_PORT=$PORT
#ENTRYPOINT ["streamlit", "run", "app.py"]

CMD ["sh", "-c", "streamlit run --server.port $PORT app.py"] 
