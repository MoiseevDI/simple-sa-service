FROM python:3.7-slim
COPY ./ /app
WORKDIR /app
RUN apt update && apt install libzbar-dev git g++ -y
RUN pip3 install -r requirements.txt && \
    python3 -m dostoevsky download fasttext-social-network-model
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["sentiment_analysis.py"]
