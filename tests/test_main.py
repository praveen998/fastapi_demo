from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
from app.utils import create_new_html
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock
from app.models import insert_category

# def test_root():
#     response=client.get("/")
#     assert response.status_code ==200
#     assert response.json() == {"hello":"world"}

# @pytest.mark.asyncio
# async def test_insert_category():
#     # Mock the database pool
#     mock_pool = AsyncMock()
#     mock_connection = AsyncMock()
#     mock_cursor = AsyncMock()
#       # Setup the mock behavior
#     mock_pool.acquire.return_value.__aenter__.return_value = mock_connection
#     mock_connection.cursor.return_value.__aenter__.return_value = mock_cursor

#       # Mock the execute and commit functions
#     mock_cursor.execute.return_value = None  # Simulates a successful insert
#     mock_connection.commit.return_value = None

#       # Call the function with mock data
#     response = await insert_category("floor cleaner", pool=mock_pool)
#        # Assertions
#     assert response["success"] is True
#     assert response["message"] == "Category inserted successfully"


#     # Ensure execute and commit were called
#     mock_cursor.execute.assert_called_once_with(
#         "INSERT INTO product_categories(categories) VALUES (%s)", ("Electronics",)
#     )
#     mock_connection.commit.assert_called_once()