from pkg.db.db import FileManager
from pkg.db.progressEnum import ProgressEnum


def db_test():
    fileManager = FileManager()
    # Create
    new_record = fileManager.create_file_record(
        path="/path/to/",
        filename="file.txt",
        sha256="d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2",
        progress=ProgressEnum.DOWNLOADED,
    )
    print(f"Created: {new_record}")

    # Read all
    file_records = fileManager.read_all_file_records()
    print("All file records:", file_records)

    # Read by ID
    record = fileManager.read_file_record_by_id(new_record.id)
    print(f"Read by ID: {record}")

    # Update
    updated_record = fileManager.update_file_record(
        record_id=new_record.id,
        path="/new/path/to/",
        filename="new_file.txt",
        sha256="e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3",
        progress=ProgressEnum.READYTOPARSE,
    )
    print(f"Updated: {updated_record}")

    # Delete
    deleted_record = fileManager.delete_file_record(new_record.id)
    print(f"Deleted: {deleted_record}")

    # Verify deletion
    file_records = fileManager.read_all_file_records()
    print("All file records after deletion:", file_records)

    test_record = fileManager.read_file_record_by_path_and_filename(
        "/sites/NAF/Shared Documents/Test2", "test.txt"
    )
    print(f"Read by path and filename: {test_record.sha256}")
