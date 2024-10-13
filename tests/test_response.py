import llm

from cli_llm.response import Response


def test_spinner_from_text(mock_model):
    # Can't get the spinner to be capture, possible because the function
    # doesn't take long enough to run the spinner.
    # So we just run the function a check there are no errors.
    mock_model.enqueue(["helloworld"])
    model = llm.get_model("mock")

    response = Response(model.prompt(""))
    result = response.text()

    assert result == "helloworld"


def test_response_interface(mock_model):
    mock_model.enqueue(["helloworld"])
    model = llm.get_model("mock")

    core_response = model.prompt("")
    response = Response(core_response)

    assert response.response == core_response
    assert repr(response) == repr(core_response)
