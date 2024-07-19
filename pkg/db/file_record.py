import uuid
from sqlalchemy import create_engine, Column, String, Enum, DateTime, func, CHAR
from progressEnum import ProgressEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FileRecord(Base):
    __tablename__ = "file_records"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    path_filename = Column(String, nullable=False)
    sha256 = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    progress = Column(
        Enum(ProgressEnum), nullable=False, default=ProgressEnum.NOTSTARTED
    )

    def __repr__(self):
        return (
            f"<FileRecord(id='{self.id}', path_filename='{self.path_filename}', sha256='{self.sha256}', "
            f"created_at='{self.created_at}', updated_at='{self.updated_at}', "
            f"progress='{self.progress.name}')>"
        )
