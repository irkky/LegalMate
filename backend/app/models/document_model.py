from datetime import datetime

class Document:
    """Non-enforced schema mirroring existing document structure"""
    
    def __init__(self, 
                 filename: str,
                 file_path: str,
                 text: str,
                 entities: dict,
                 summary: str,
                 risks: list,
                 upload_time: datetime,
                 status: str = "processed"):
        self.filename = filename
        self.file_path = file_path
        self.text = text
        self.entities = entities
        self.summary = summary
        self.risks = risks
        self.upload_time = upload_time
        self.status = status

    def to_dict(self):
        """Mirror original dictionary structure"""
        return {
            "filename": self.filename,
            "file_path": self.file_path,
            "text": self.text,
            "entities": self.entities,
            "summary": self.summary,
            "risks": self.risks,
            "upload_time": self.upload_time,
            "status": self.status
        }