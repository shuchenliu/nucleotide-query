FROM python:3.9-slim
LABEL authors="will liu"

WORKDIR /app
COPY entrypoint.sh .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]