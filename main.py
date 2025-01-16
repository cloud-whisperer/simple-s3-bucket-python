import boto3
import sys
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# AWS Configuration
# Default region.
aws_region = "us-east-1" 
bucket_name = "beginner-devops-bucket"
image_path = "file_storage_gateway_KMS_SMB_modified_lc.jpg"
upload_key = "uploaded-images/file_storage_gateway_KMS_SMB_modified_lc.jpg"

def get_user_credentials():
    """
   Prompt the user to input AWS credentials securely. 
    """

    print("Please enter the AWS credentials:")
    aws_access_key_id = input("AWS Access Key ID:").strip()
    aws_secret_access_key = input("AWS Secret Access Key: ").strip()
    return aws_access_key_id, aws_secret_access_key

def create_s3_client(aws_access_key_id, aws_secret_access_key, region):
    """
   Create an S3 client using the provided credentials and region.
    """
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region
        )
        return s3_client 
    except Exception as e:
        print(f"Error creating S3 client: {e}")
        sys.exit(1)

def create_s3_bucket(s3_client, region, bucket_name):
    """
   Create an S3 bucket in the specified region. 
    """
    try:
        # No LocationConstraint for us-east-1
        if region == 'us-east-1': 
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            response = s3_client.create_bucket( 
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        print(f"Bucket '{bucket_name}' created successfully in region '{region}'.")
        return response 
    except Exception as e:
        print(f"Error creating bucket: {e}")
        sys.exit(1)




def upload_image_to_s3(s3_client, bucket_name, image_path, upload_key):
    """
   Upload an image to the specified S3 bucket. 
    """
    try:
        with open(image_path, "rb") as image_file:
            s3_client.upload_fileobj(
            image_file,
            bucket_name,
            upload_key,
            ExtraArgs={"ACL": "private", "ContentType":"image/jpeg"}
            )
        print(f"Image '{image_path}' uploaded successfully to bucket '{bucket_name}' as '{upload_key}'.")
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        sys.exit(1)
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
        sys.exit(1)
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
        sys.exit(1)
    except Exception as e:
        print(f"Error uploading image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Prompt the user for the AWS credentials.
    aws_access_key_id, aws_secret_access_key = get_user_credentials()

    # Create an S3 client.
    s3_client = create_s3_client(aws_access_key_id, aws_secret_access_key, aws_region) 

    # Create an S3 bucket.
    print("Starting the S3 bucket creation process...")
    create_s3_bucket(s3_client, aws_region, bucket_name)

    # Upload the image to the S3 bucket.
    print("Uploading the image to the S3 bucket...")
    upload_image_to_s3(s3_client, bucket_name, image_path, upload_key)
