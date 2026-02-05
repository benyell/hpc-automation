import boto3
import os
import glob

# Use an Environment Variable if provided, otherwise default to /tmp
BACKUP_DIR = os.getenv('BACKUP_DIR', '/tmp/hpc_backups/')
BUCKET_NAME = 'yash-proxmox-backups'

def upload_latest():
    s3 = boto3.client('s3')
    files = glob.glob(os.path.join(BACKUP_DIR, '*.vma.zst'))
    
    if not files:
        print(f"No backups found in {BACKUP_DIR}")
        return

    latest_file = max(files, key=os.path.getctime)
    file_name = os.path.basename(latest_file)

    print(f"Uploading {file_name} to S3...")
    s3.upload_file(latest_file, BUCKET_NAME, file_name)
    print("Upload Complete!")

if __name__ == "__main__":
    upload_latest()