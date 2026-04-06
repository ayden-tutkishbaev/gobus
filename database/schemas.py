from pydantic import BaseModel, ConfigDict, Field


class SchoolBase(BaseModel):
    name: str = Field(max_length=240)

class SchoolCreate(SchoolBase):
    pass

class SchoolRead(SchoolBase):
    model_config = ConfigDict(from_attributes=True)
    id: int