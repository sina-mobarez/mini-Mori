from core.repositories.text_repository import TextRepository
from core.schemas import TextOutput

class TextService:
    def __init__(self):
        self.repository = TextRepository()

    async def process_text(self, text: str) -> TextOutput:
        processed_text = await self.repository.process_text(text)
        return TextOutput(result=processed_text)
