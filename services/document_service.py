from typing import BinaryIO, List
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sqlalchemy.ext.asyncio import AsyncSession
from models.document import Document, DocumentChunk
from core.logging import logger
from uuid import UUID
import io


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2048,
            chunk_overlap=256,
            length_function=len,
        )

    async def process_pdf(
        self, file: BinaryIO, user_id: UUID, filename: str
    ) -> Document:
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            logger.debug(
                f"Processing PDF with {len(pdf_reader.pages)} pages for user {user_id}"
            )
            for page in pdf_reader.pages:
                text_content += page.extract_text()
            logger.debug(f"Successfully extracted text from PDF for user {user_id}")
            document = Document(user_id=user_id, filename=filename, file_type="pdf")
            self.db.add(document)
            await self.db.flush()
            logger.debug(f"Successfully added document to database for user {user_id}")
            chunks = self.text_splitter.split_text(text_content)
            logger.debug(f"Split text into {len(chunks)} chunks for user {user_id}")
            for idx, chunk_content in enumerate(chunks):
                chunk = DocumentChunk(
                    document_id=document.id,
                    content=chunk_content,
                    chunk_index=idx,
                )
                self.db.add(chunk)
                logger.debug(f"Added chunk {idx} to database for user {user_id}")
            await self.db.commit()
            logger.info(
                f"Successfully processed PDF document: {filename} for user {user_id}"
            )
            return document

        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error processing PDF document: {str(e)} for user {user_id}")
            raise
