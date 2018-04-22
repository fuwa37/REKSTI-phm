# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a client
storage_client = storage.Client.from_service_account_json(
'kunciimka.json')

bucket_name="imka-e61ac.appspot.com"

bucket = storage_client.get_bucket(bucket_name)
print(bucket)

blob = bucket.blob("folderName/" + 'aaa.txt')
blob.upload_from_filename("tes.py")