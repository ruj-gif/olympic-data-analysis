from azure.storage.filedatalake import DataLakeServiceClient
import os

from config import STORAGE_ACCOUNT_NAME, ACCOUNT_KEY, FILE_SYSTEM

DIRECTORY = "raw-data"

service_client = DataLakeServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
    credential=ACCOUNT_KEY
)

filesystem = service_client.get_file_system_client(FILE_SYSTEM)

os.makedirs("data/raw", exist_ok=True)

paths = filesystem.get_paths(path=DIRECTORY)

for path in paths:
    if not path.is_directory:
        file_client = filesystem.get_file_client(path.name)

        with open(
            f"data/raw/{os.path.basename(path.name)}",
            "wb"
        ) as f:
            f.write(file_client.download_file().readall())

        print(f"Downloaded {path.name}")