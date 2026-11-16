from pydantic import BaseModel, Field, ConfigDict


class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    company_name: str | None = Field(default=None, max_length=150)
    description: str = Field(min_length=50)


class JobUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    company_name: str | None = Field(default=None, max_length=150)
    description: str = Field(min_length=50)


class JobResponse(BaseModel):
    id: int
    title: str
    company_name: str | None
    description: str

    model_config = ConfigDict(from_attributes=True)