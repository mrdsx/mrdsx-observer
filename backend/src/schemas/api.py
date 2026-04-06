from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

api_model_config = ConfigDict(
    alias_generator=to_camel,
    validate_by_alias=True,
    validate_by_name=True,
)
