FROM prefecthq/prefect:2.8-python3.10

EXPOSE 4200

RUN apt update && apt install -y curl
WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh

CMD ["sh","/app/entrypoint.sh"]
