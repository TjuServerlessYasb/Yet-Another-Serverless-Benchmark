from xmlrpc.client import ResponseError

from minio import Minio

minioClient = Minio("10.244.4.7:9000", access_key="admin123", secret_key="admin123", secure=False)
print(111)

# try:
#     minioClient.make_bucket("data-500m", location="us-east-123")
# except ResponseError as err:
#     print(err)

buckets = minioClient.list_buckets()
for bucket in buckets:
    print(bucket.name, bucket.creation_date)
    try:
        minioClient.remove_bucket(bucket.name)
    except ResponseError as err:
        print(err)