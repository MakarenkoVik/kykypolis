FROM python:3.11.3-slim AS base
WORKDIR /

FROM base

COPY ./requirements.txt .

COPY . .

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
