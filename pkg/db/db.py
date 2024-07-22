from sqlalchemy import create_engine, Column, String, Enum, DateTime, func, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pkg.db.file_record import FileRecord, Base
from pkg.db.progressEnum import ProgressEnum


engine = create_engine("sqlite:///example.db", echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


class FileManager:
    def __init__(self):
        # Create a Session
        self.session = Session()

    def create_file_record(self, path, filename, sha256, progress):
        new_record = FileRecord(
            path=path, filename=filename, sha256=sha256, progress=progress
        )
        self.session.add(new_record)
        self.session.commit()
        return new_record

    def read_all_file_records(self):
        return self.session.query(FileRecord).all()

    def read_file_record_by_id(self, record_id):
        return self.session.query(FileRecord).filter_by(id=record_id).first()

    def update_file_record(
        self, record_id, path=None, filename=None, sha256=None, progress=None
    ):
        record_to_update = (
            self.session.query(FileRecord).filter_by(id=record_id).first()
        )
        if record_to_update:
            if path:
                record_to_update.path = path
            if filename:
                record_to_update.filename = filename
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
