from pydantic import BaseModel


class ExampleModel(BaseModel):
    title: str = 'Title example'
    description = 'Description example'
    number: int = 100
