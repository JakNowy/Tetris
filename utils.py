class RetryOnException:
    """
    Appropriate only for exceptions that are capable of handling themselves in next iterations.
    """

    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __call__(self, callable):
        def wrapper(*args, **kwargs):
            try:
                result = callable(*args, **kwargs)
            except self.exceptions:
                return wrapper(*args, **kwargs)
            else:
                return result

        return wrapper


class CollisionError(Exception):
    pass


class BoundCollisionError(Exception):
    pass

