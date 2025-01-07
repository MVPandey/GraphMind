from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from services.document_service import DocumentService
from core.database import get_db
from core.logging import logger
from typing import List
from uuid import UUID

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/")
async def upload_document(
    user_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        document_service = DocumentService(db)
        document = await document_service.process_pdf(file.file, user_id, file.filename)

        return {
            "message": "Document processed successfully",
            "document_id": document.id,
        }

    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing document")
