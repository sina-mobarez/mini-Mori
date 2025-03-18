import unittest
from unittest.mock import patch, MagicMock
from core.services.image_service import ImageService

class TestImageService(unittest.TestCase):
    """
    Unit test for the ImageService class.
    """

    @patch('core.repositories.image_repository.ImageRepository')
    @patch('core.utils.clip_model_wrapper')
    def setUp(self, MockClipModelWrapper, MockImageRepository):
        """
        Set up the test case with mocked dependencies.

        :param MockClipModelWrapper: Mock for the CLIP model wrapper.
        :param MockImageRepository: Mock for the ImageRepository.
        """
        self.mock_repository = MockImageRepository.return_value
        self.mock_clip = MockClipModelWrapper
        self.service = ImageService()

    @patch('core.utils.clip_model_wrapper')
    async def test_search_similar_images(self, MockClipModelWrapper):
        """
        Test the search_similar_images method of ImageService.

        This test ensures that the search_similar_images method correctly calls the repository
        and returns the expected results.

        :param MockClipModelWrapper: Mock for the CLIP model wrapper.
        """
        # Mock the generate_text_embedding method
        MockClipModelWrapper.generate_text_embedding.return_value = [0.1] * 512
        
        # Mock the search_similar_images method of the repository
        self.mock_repository.search_similar_images.return_value = [
            MagicMock(id="1", score=0.9),
            MagicMock(id="2", score=0.8)
        ]

        # Call the method under test
        results = await self.service.search_similar_images("test query")

        # Assert that the repository's search_similar_images method was called once
        self.mock_repository.search_similar_images.assert_called_once()
        
        # Assert the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], "1")
        self.assertEqual(results[0]['score'], 0.9)

if __name__ == '__main__':
    unittest.main()
