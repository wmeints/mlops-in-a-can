FROM prefecthq/prefect:2.8-python3.10

COPY deploy_blocks.py /opt/workflow-server-init/deploy_blocks.py
COPY entrypoint.sh /opt/workflow-server-init/entrypoint.sh

CMD ["sh", "/opt/workflow-server-init/entrypoint.sh"]