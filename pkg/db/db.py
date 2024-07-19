from sqlalchemy import create_engine, Column, String, Enum, DateTime, func, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from file_record import FileRecord, Base
from progressEnum import ProgressEnum


engine = create_engine("sqlite:///example.db", echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


class FileManager:
    def __init__(self):
        # Create a Session
        self.session = Session()

    def create_file_record(self, path_filename, sha256, progress):
        new_record = FileRecord(
            path_filename=path_filename, sha256=sha256, progress=progress
        )
        self.session.add(new_record)
        self.session.commit()
        return new_record

    def read_all_file_records(self):
        return self.session.query(FileRecord).all()

    def read_file_record_by_id(self, record_id):
        return self.session.query(FileRecord).filter_by(id=record_id).first()

    def update_file_record(
        self, record_id, path_filename=None, sha256=None, progress=None
    ):
        record_to_update = (
            self.session.query(FileRecord).filter_by(id=record_id).first()
        )
        if record_to_update:
            if path_filename:
                record_to_update.path_filename = path_filename
            if sha256:
                record_to_update.sha256 = sha256
            if progress:
                record_to_update.progress = progress
            self.session.commit()
        return record_to_update

    def delete_file_record(self, record_id):
        record_to_delete = (
            self.session.query(FileRecord).filter_by(id=record_id).first()
        )
        if record_to_delete:
            self.session.delete(record_to_delete)
            self.session.commit()
        return record_to_delete


# Example usage of CRUD operations
if __name__ == "__main__":
    fileManager = FileManager()
    # Create
    new_record = fileManager.create_file_record(
        path_filename="/path/to/file.txt",
        sha256="d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2",
        progress=ProgressEnum.NOTSTARTED,
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
        path_filename="/new/path/to/file.txt",
        sha256="e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3",
        progress=ProgressEnum.INPROGRESS,
    )
    print(f"Updated: {updated_record}")

    # Delete
    deleted_record = fileManager.delete_file_record(new_record.id)
    print(f"Deleted: {deleted_record}")

    # Verify deletion
    file_records = fileManager.read_all_file_records()
    print("All file records after deletion:", file_records)
