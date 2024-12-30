from pydantic import BaseModel, ConfigDict, Field


class PascalCaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=str.capitalize
    )


class Title(PascalCaseModel):
    english: str = Field()
    gurmukhi: str = Field()


class Bani(PascalCaseModel):
    id: str = Field()
    title: Title = Field()
