from utilities.schemas import CamelCaseBaseModel


class CreateArtistBody(CamelCaseBaseModel):
    display_name: str
    slug: str
