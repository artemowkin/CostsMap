from pydantic import BaseModel
from humps import camelize


class CamelModel(BaseModel):
    """Base model with camelized fields"""

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
