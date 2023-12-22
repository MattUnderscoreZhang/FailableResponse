from failable_response.pydantic_response import Response, UnknownType, combine_responses


Status = str


def fail_function() -> Response[Status]:
    return Response(success=False, data=Status("failed"))


def success_function() -> Response[Status]:
    return Response(success=True, data=Status("success"))


def test_default_type() -> None:
    response = Response(success=True, data=6)
    assert type(response) == Response[UnknownType]


def test_type_checker() -> None:
    response = fail_function()
    try:
        response.data.do_thing()
        response.data.do_nonexistent_thing()
    except AttributeError:
        pass


def test_response_type() -> None:
    response = fail_function()
    assert response.success is False
    assert response.data == Status("failed")
    assert type(response) == Response
    assert type(response.data) == Status

    response = success_function()
    assert response.success is True
    assert response.data == Status("success")
    assert type(response) == Response
    assert type(response.data) == Status


def test_combine_responses() -> None:
    responses = [fail_function(), success_function()]
    combined_response = combine_responses(responses)
    assert combined_response.success is False
    assert combined_response.data == [Status("failed"), Status("success")]

    responses = [success_function(), success_function()]
    combined_response = combine_responses(responses)
    assert combined_response.success is True
    assert combined_response.data == [Status("success"), Status("success")]

    responses = [fail_function(), fail_function()]
    combined_response = combine_responses(responses)
    assert combined_response.success is False
    assert combined_response.data == [Status("failed"), Status("failed")]
