from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import mysql.connector
import authInfo

# account_name = authInfo.azure_account_name
# account_key = authInfo.azure_account_key
# container_name = authInfo.azure_container_name

# # Create Blob Service Client
# blob_service_client = BlobServiceClient(account_url = f"https://{account_name}.blob.core.windows.net", credential = account_key)
# # Create a Container Client
# container_client = blob_service_client.get_container_client(container_name)

# # Code Test Place
# blob_list = container_client.list_blobs()
# for blob in blob_list:
#     print(blob.name)

mysql_host = authInfo.sql_host
mysql_user = authInfo.sql_user
mysql_password = authInfo.sql_password
mysql_database = authInfo.sql_database

db_config = {
    'host' : authInfo.sql_host,
    'user' : authInfo.sql_user,
    'password' : authInfo.sql_password,
    'database' : authInfo.sql_database,
    'port': 3306
}

# Establish a connection
connection = mysql.connector.connect(**db_config)

# Create a cursor object
cursor = connection.cursor()
