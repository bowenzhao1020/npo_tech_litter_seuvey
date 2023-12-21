from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import authInfo

account_name = authInfo.azure_account_name
account_key = authInfo.azure_account_key
container_name = authInfo.azure_container_name

# Create Blob Service Client
blob_service_client = BlobServiceClient(account_url = f"https://{account_name}.blob.core.windows.net", credential = account_key)
# Create a Container Client
container_client = blob_service_client.get_container_client(container_name)

# Code Test Place
blob_list = container_client.list_blobs()
for blob in blob_list:
    print(blob.name)