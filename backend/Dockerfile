FROM python:3.9-slim
LABEL authors="will liu"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY . .
ENTRYPOINT ["./entrypoint.sh"]


