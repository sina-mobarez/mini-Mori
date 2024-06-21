from fastapi import FastAPI, UploadFile, File
from core.schemas import TextInput, TextOutput, ImageOutput
from core.services.text_service import TextService
from core.services.image_service import ImageService

app = FastAPI()

text_service = TextService()
image_service = ImageService()

@app.post("/process-text", response_model=TextOutput)
async def process_text(text_input: TextInput):
    return await text_service.process_text(text_input.text)

@app.post("/process-image", response_model=ImageOutput)
async def process_image(file: UploadFile = File(...)):
    image_data = await file.read()
    return await image_service.process_image(image_data)
