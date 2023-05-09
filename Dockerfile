FROM python:3.11.3-slim AS base
WORKDIR /
RUN ls

FROM base

COPY ./requirements.txt .

COPY . .

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

RUN ls -l 

ENTRYPOINT ["./entrypoint.sh"]
