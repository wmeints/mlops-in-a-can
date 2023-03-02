FROM mcr.microsoft.com/azure-cli:latest

COPY entrypoint.sh /opt/datalake-init/entrypoint.sh
COPY data/iris.csv /opt/datalake-init/data/iris.csv

CMD ["sh", "/opt/datalake-init/entrypoint.sh"]