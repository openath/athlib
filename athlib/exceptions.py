class RuleViolation(Exception):
    """Exception to indicate incorrect athletics logic

    This may be used if, for example, there is a fourth
    attempt at a high jump.  We use this as a form of
    assertion within the code; others are welcome to as well.
    """
    pass

