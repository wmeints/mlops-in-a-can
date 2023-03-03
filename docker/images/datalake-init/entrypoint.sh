# Create the data lake storage containers
az storage container create --name flows
az storage container create --name raw
az storage container create --name intermediate
az storage container create --name preprocessed

# Upload some sample data to the datalake.
az storage blob upload --container-name raw --name iris/2023/03/02/iris.csv --file /opt/datalake-init/data/iris.csv --overwrite