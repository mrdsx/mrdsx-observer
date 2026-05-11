from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel

api_model_config = ConfigDict(
    alias_generator=to_camel,
    validate_by_alias=True,
    validate_by_name=True,
)

uptime_field = Field(ge=0, le=100)
