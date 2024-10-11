import llm
import pytest
from llm.plugins import pm
from pydantic import Field


# Using the mock model defined in llm's tests.
class MockModel(llm.Model):
    model_id = "mock"

    class Options(llm.Options):
        max_tokens: int | None = Field(description="Maximum number of tokens to generate.", default=None)

    def __init__(self):
        self.history = []
        self._queue = []

    def enqueue(self, messages):
        assert isinstance(messages, list)
        self._queue.append(messages)

    def execute(self, prompt, stream, response, conversation):
        self.history.append((prompt, stream, response, conversation))
        while True:
            try:
                messages = self._queue.pop(0)
                yield from messages
                break
            except IndexError:
                break


@pytest.fixture
def mock_model():
    return MockModel()


@pytest.fixture(autouse=True)
def register_embed_demo_model(mock_model):
    class MockModelsPlugin:
        __name__ = "MockModelsPlugin"

        @llm.hookimpl
        def register_models(self, register):
            register(mock_model)

    pm.register(MockModelsPlugin(), name="undo-mock-models-plugin")
    try:
        yield
    finally:
        pm.unregister(name="undo-mock-models-plugin")
