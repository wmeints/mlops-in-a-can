# Create the data lake storage containers
az storage container create --name flows
az storage container create --name bronze
az storage container create --name silver
az storage container create --name gold
az storage container create --name sandbox

# Upload some sample data to the datalake.
az storage blob upload --container-name gold --name iris/2023/03/02/iris.csv --file /opt/datalake-init/data/iris.csv --overwrite