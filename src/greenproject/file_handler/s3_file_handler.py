import boto3
import os
import sys
from pathlib import Path
import shutil
from appLogger import AppLogger

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from greenproject.config import config

appLogger = AppLogger()

import boto3



def is_folder_empty(bucket_name, folder_prefix):
    s3_client = create_s3_client()

    # List objects in the folder (prefix)
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix, Delimiter='/')

    # If the 'Contents' field is empty, the folder is empty
    if 'Contents' not in response:
        return True  # Folder is empty
    
    # Check if there are objects under the folder prefix
    if len(response['Contents']) == 0:
        return True  # Folder is empty

    return False  # Folder contains objects







def create_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,  # Hardcoded AWS Access Key
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,  # Hardcoded AWS Secret Key
        region_name=config.REGION_NAME  # Region for your S3 bucket
    )

def download_all_s3_validation_files():
    s3_client = create_s3_client()
    download_files_from_s3(s3_client, config.bucket_name, config.validation_prefix, config.local_dir)
    
def download_all_s3_files():
    s3_client = create_s3_client()
    download_files_from_s3(s3_client, config.bucket_name, config.prefix, config.local_dir)
    download_files_from_s3(s3_client, config.bucket_name, config.offset_prefix, config.local_dir)
    download_files_from_s3(s3_client, config.bucket_name, config.metadata_prefix, config.local_dir)

def download_files_from_s3(s3_client, bucket_name, prefix, local_dir):
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..','..'))
    local_dir = os.path.join(parent_dir, local_dir)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    continuation_token = None
    while True:
        list_params = {
            'Bucket': bucket_name,
            'Prefix': prefix,
            'Delimiter': '',  # No delimiter, to include all objects under the prefix
        }
        if continuation_token:
            list_params['ContinuationToken'] = continuation_token
        response = s3_client.list_objects_v2(**list_params)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3_key = obj['Key']
                local_file_path = os.path.join(local_dir, s3_key)
                local_subdir = os.path.dirname(local_file_path)
                if not os.path.exists(local_subdir):
                    os.makedirs(local_subdir)
                try:
                    s3_client.download_file(bucket_name, s3_key, local_file_path)
                    
                except Exception as e:
                    appLogger.getLogger().debug(f"Error downloading {s3_key}: {e}")
                    print(f"Error downloading {s3_key}: {e}")

        if response.get('IsTruncated'): 
            continuation_token = response.get('NextContinuationToken')
        else:
            break


def delete_local_dir_content(local_dir):
    
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
    local_dir_path = os.path.join(parent_dir, local_dir)
    
    if os.path.exists(local_dir_path):
        try:
            shutil.rmtree(local_dir_path)
            appLogger.getLogger().debug(f"Successfully deleted content in {local_dir_path}")  
            print(f"Successfully deleted content in {local_dir_path}")
        except Exception as e:
            appLogger.getLogger().debug(f"Error deleting {local_dir_path}: {e}")
            print(f"Error deleting {local_dir_path}: {e}")
    else:
        appLogger.getLogger().debug(f"Directory {local_dir_path} does not exist.")
        print(f"Directory {local_dir_path} does not exist.")

def upload_folder_to_s3():

    s3_client = create_s3_client()
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..','..'))
    local_dir = os.path.join(parent_dir, config.output_local_dir)
    
    # Walk through the local directory to find all files
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_file_path = os.path.join(root, file)
            # Generate the S3 key by removing the base directory part
            relative_path = os.path.relpath(local_file_path, local_dir)
            s3_key = os.path.join(config.output_prefix, relative_path)
            try:
                s3_client.upload_file(local_file_path, config.bucket_name, s3_key)
                appLogger.getLogger().debug(f"Successfully uploaded {local_file_path} to s3://{config.bucket_name}/{s3_key}")
                print(f"Successfully uploaded {local_file_path} to s3://{config.bucket_name}/{s3_key}")

                os.remove(local_file_path)
                appLogger.getLogger().debug(f"Successfully removed {local_file_path}")
                print(f"Successfully removed {local_file_path}")
            except Exception as e:
                appLogger.getLogger().debug(f"Error uploading {local_file_path} to S3: {e}")
                print(f"Error uploading {local_file_path} to S3: {e}")

def move_processed_folder_to_completed(bucket_name, prefix, prefix_completed):
    s3_client = create_s3_client()
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    for item in response.get('Contents', []):
        source_key = item['Key']
        destination_key = source_key.replace(prefix, prefix_completed, 1)
        
        # Copy the object to the new destination
        s3_client.copy_object(Bucket=bucket_name, CopySource=f'{bucket_name}/{source_key}', Key=destination_key)
        
        # Delete the original object after copying
        s3_client.delete_object(Bucket=bucket_name, Key=source_key)


print("Files moved successfully.")

if __name__ == '__main__':
    
    s3_client = create_s3_client()
   # delete_local_dir_content(config.local_dir)
    download_files_from_s3(s3_client, config.bucket_name, config.prefix, config.local_dir)
    download_files_from_s3(s3_client, config.bucket_name, config.offset_prefix, config.local_dir)
    download_files_from_s3(s3_client, config.bucket_name, config.metadata_prefix, config.local_dir)



