from api_backend.observability.metrics import NonExceptionThrowingCounter as Counter
from api_backend.common.models import ModelResponse


class Metrics:
    def __init__(self):
        self.requests_started = Counter(
            "aviary_requests_started",
            description="Number of requests started.",
            tag_keys=("model_id",),
        )
        self.requests_finished = Counter(
            "aviary_requests_finished",
            description="Number of requests finished",
            tag_keys=("model_id",),
        )
        self.requests_errored = Counter(
            "aviary_requests_errored",
            description="Number of requests errored",
            tag_keys=("model_id",),
        )

        self.tokens_generated = Counter(
            "aviary_tokens_generated",
            description="Number of tokens generated by Aviary",
            tag_keys=("model_id",),
        )
        self.tokens_input = Counter(
            "aviary_tokens_input",
            description="Number of tokens input by the user",
            tag_keys=("model_id",),
        )

    def track(self, res: ModelResponse, is_first_token: bool, model: str):
        model_tags = {"model_id": model}
        # Update metrics
        if res.num_generated_tokens:
            self.tokens_generated.inc(res.num_generated_tokens, tags=model_tags)
        if is_first_token and res.num_input_tokens:
            self.tokens_input.inc(res.num_input_tokens, tags=model_tags)

        if res.error:
            self.requests_errored.inc(tags=model_tags)

        if res.finish_reason is not None:
            self.requests_finished.inc(tags=model_tags)
