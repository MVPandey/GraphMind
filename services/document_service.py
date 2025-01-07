from typing import BinaryIO, List
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session
from models.document import Document, DocumentChunk
from core.logging import logger
from uuid import UUID
import io


class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    async def process_pdf(
        self, file: BinaryIO, user_id: UUID, filename: str
    ) -> Document:
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""

            for page in pdf_reader.pages:
                text_content += page.extract_text()

            document = Document(user_id=user_id, filename=filename, file_type="pdf")
            self.db.add(document)

            chunks = self.text_splitter.split_text(text_content)

            for idx, chunk_content in enumerate(chunks):
                chunk = DocumentChunk(
                    document_id=document.id,
                    content=chunk_content,
                    chunk_index=idx,
                )
                self.db.add(chunk)

            await self.db.commit()
            logger.info(f"Successfully processed PDF document: {filename}")
            return document

        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error processing PDF document: {str(e)}")
            raise
