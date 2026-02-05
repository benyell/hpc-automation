import boto3
import os
import glob
import gnupg

# Configuration
BACKUP_DIR = os.getenv('BACKUP_DIR', '/tmp/hpc_backups/')
BUCKET_NAME = 'yash-proxmox-backups'
PASSPHRASE = os.getenv("GPG_PASSPHRASE")

gpg = gnupg.GPG()

def encrypt_file(file_path):
    encrypted_path = f"{file_path}.gpg"
    print(f"Encrypting {os.path.basename(file_path)}...")
    with open(file_path, 'rb') as f:
        status = gpg.encrypt_file(
            f, 
            recipients=None, 
            symmetric=True,
            passphrase=PASSPHRASE,
            output=encrypted_path
        )
    if status.ok:
        return encrypted_path
    else:
        raise Exception(f"Encryption failed: {status.stderr}")

def upload_latest():
    s3 = boto3.client('s3')
    # Find the latest unencrypted backup
    files = glob.glob(os.path.join(BACKUP_DIR, '*.vma.zst'))
    
    if not files:
        print(f"No backups found in {BACKUP_DIR}")
        return

    latest_file = max(files, key=os.path.getctime)
    
    # --- THE KEY STEP ---
    # 1. Encrypt it first
    encrypted_file_path = encrypt_file(latest_file)
    encrypted_file_name = os.path.basename(encrypted_file_path)

    # 2. Upload the encrypted version
    print(f"Uploading encrypted file {encrypted_file_name} to S3...")
    s3.upload_file(encrypted_file_path, BUCKET_NAME, encrypted_file_name)
    print("Upload Complete!")
    
    # 3. Clean up the local encrypted file (optional but recommended)
    os.remove(encrypted_file_path)
    print(f"Cleaned up local encrypted file: {encrypted_file_name}")

if __name__ == "__main__":
    upload_latest()