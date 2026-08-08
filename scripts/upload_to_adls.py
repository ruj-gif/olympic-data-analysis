import os
from azure.storage.filedatalake import DataLakeServiceClient
from config import STORAGE_ACCOUNT_NAME, ACCOUNT_KEY, FILE_SYSTEM

service_client = DataLakeServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
    credential=ACCOUNT_KEY
)

file_system = service_client.get_file_system_client(FILE_SYSTEM)

LOCAL_FOLDER = "data/transformed"

# Loop through folders: athletes, coaches, medals, etc.
for folder in os.listdir(LOCAL_FOLDER):

    folder_path = os.path.join(LOCAL_FOLDER, folder)

    # Skip if it's not a folder
    if not os.path.isdir(folder_path):
        continue

    print(f"\nUploading folder: {folder}")

    # Azure directory path
    # Example: transformed-data/athletes
    adls_directory_path = f"transformed-data/{folder}"

    directory_client = file_system.get_directory_client(
        adls_directory_path
    )

    # Create directory in Azure
    try:
        directory_client.create_directory()
        print(f"Created directory: {adls_directory_path}")
    except:
        print(f"Directory already exists: {adls_directory_path}")

    # Loop through ALL files inside the local folder
    for file_name in os.listdir(folder_path):

        local_file_path = os.path.join(
            folder_path,
            file_name
        )

        # Skip subdirectories
        if not os.path.isfile(local_file_path):
            continue

        # Skip Hadoop .crc checksum files
        if file_name.endswith(".crc"):
            continue

        # Azure destination
        adls_file_path = (
            f"transformed-data/{folder}/{file_name}"
        )

        print(f"Uploading: {file_name}")

        file_client = file_system.get_file_client(
            adls_file_path
        )

        with open(local_file_path, "rb") as data:
            file_client.upload_data(
                data,
                overwrite=True
            )

        print(f"Uploaded: {adls_file_path}")

print("\nAll transformed datasets uploaded successfully!")