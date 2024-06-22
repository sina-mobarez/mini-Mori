import pytest
from httpx import AsyncClient
from unittest.mock import patch
from core.main import app

@pytest.mark.asyncio
async def test_search_images_endpoint():
    """
    Test the /search-images endpoint.

    This test verifies that the endpoint correctly processes a text query and returns the expected
    results. It mocks the ImageService to return predefined results and then checks if the endpoint
    response status code is 200.
    """
    with patch('core.services.image_service.ImageService') as MockImageService:
        # Create a mock service and define return value for the search_similar_images method
        mock_service = MockImageService.return_value
        mock_service.search_similar_images.return_value = [
            {"id": "1", "score": 0.9},
            {"id": "2", "score": 0.8}
        ]

        # Use AsyncClient to simulate sending a request to the FastAPI app
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/search-images", json={"text": "test query"})

        # Check if the response status code is 200
        assert response.status_code == 200
