import uuid
from sqlalchemy import create_engine, Column, String, Enum, DateTime, func, CHAR
from pkg.db.csv_type import CSVType
from pkg.db.progressEnum import ProgressEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FileRecord(Base):
    __tablename__ = "file_records"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    path = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    sha256 = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    progress = Column(
        Enum(ProgressEnum), nullable=False, default=ProgressEnum.DOWNLOADED
    )
    csv_type = Column(Enum(CSVType), nullable=True)
    filetype = Column(String, nullable=False)

    def __repr__(self):
        return (
            f"<FileRecord(id='{self.id}', path='{self.path}', filename='{self.filename}', sha256='{self.sha256}', "
            f"created_at='{self.created_at}', updated_at='{self.updated_at}', "
            f"progress='{self.progress.name}', filetype='{self.filetype}' , csv_type='{self.csv_type}')>"  # Added 'filetype' to the representation
        )
