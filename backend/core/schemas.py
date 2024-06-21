from pydantic import BaseModel

class TextInput(BaseModel):
    text: str

class TextOutput(BaseModel):
    result: str

class ImageOutput(BaseModel):
    result: str
