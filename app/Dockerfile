FROM python:3.11.2-slim-bullseye

WORKDIR /app

# ADD Somenew 
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app/. .

CMD ["python", "src/main.py"]
