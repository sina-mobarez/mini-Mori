import unittest
from unittest.mock import patch, MagicMock
from core.repositories.image_repository import ImageRepository

class TestImageRepository(unittest.TestCase):
    """
    Unit test for the ImageRepository class.
    """

    @patch('qdrant_client.QdrantClient')
    def setUp(self, MockQdrantClient):
        """
        Set up the test case with a mocked QdrantClient.

        :param MockQdrantClient: Mock for the QdrantClient.
        """
        self.mock_client = MockQdrantClient.return_value
        self.repo = ImageRepository()

    @patch('qdrant_client.http.models.PointStruct')
    async def test_upsert_images(self, MockPointStruct):
        """
        Test the upsert_images method of ImageRepository.

        This test ensures that the upsert_images method correctly calls the QdrantClient's upsert method.

        :param MockPointStruct: Mock for the PointStruct.
        """
        points = [MockPointStruct(id="1", vector=[0.1] * 512, payload={"product_id": 1, "url": "http://example.com"})]
        await self.repo.upsert_images(points)
        self.mock_client.upsert.assert_called_once_with(collection_name='images', points=points)

    async def test_search_similar_images(self):
        """
        Test the search_similar_images method of ImageRepository.

        This test ensures that the search_similar_images method correctly calls the QdrantClient's search method.
        """
        embedding = [0.1] * 512
        await self.repo.search_similar_images(embedding)
        self.mock_client.search.assert_called_once_with(collection_name='images', query_vector=embedding, limit=5)

if __name__ == '__main__':
    unittest.main()
