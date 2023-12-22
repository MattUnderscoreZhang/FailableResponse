from dataclasses import dataclass
from typing import Generic, TypeVar


UnknownType = dict
# T = TypeVar("T", default=UnknownType)  # PEP 696 - won't be supported until at least 3.13
T = TypeVar("T")
@dataclass
class Response(Generic[T]):
    success: bool
    data: T


U = TypeVar("U")
def combine_responses(responses: list[Response[U]]) -> Response[list[U]]:
    return Response(
        success=all([response.success for response in responses]),
        data=[response.data for response in responses],
    )
