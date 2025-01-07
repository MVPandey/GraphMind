import asyncio
import httpx
import json
from pathlib import Path


async def test_document_upload():
    # Create a test user first
    async with httpx.AsyncClient(timeout=3600) as client:
        # 1. Create user
        user_response = await client.post(
            "http://localhost:8000/users",
            json={"email": "test12@example.com", "name": "Test User"},
        )
        assert user_response.status_code == 200
        user_data = user_response.json()
        user_id = user_data["user_id"]

        # 2. Upload PDF
        test_pdf_path = Path("tests/data/moby10b.pdf")
        with open(test_pdf_path, "rb") as f:
            files = {"file": ("test.pdf", f, "application/pdf")}
            response = await client.post(
                f"http://localhost:8000/documents?user_id={user_id}", files=files
            )

        assert response.status_code == 200
        print("Document uploaded successfully:", response.json())


if __name__ == "__main__":
    asyncio.run(test_document_upload())
