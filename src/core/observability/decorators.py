from functools import wraps
def trace_node(
    node_name: str,
):

    def decorator(func):

        @wraps(func)
        async def wrapper(
            self,
            state,
        ):

            with (
                self.agent
                .runtime
                .tracer
                .span(node_name)
            ):

                return await func(
                    self,
                    state,
                )

        return wrapper

    return decorator