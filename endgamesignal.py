class EndLevel(Exception):
    """
    Exception to signal that the level is over
    This allows us to end the level from any point in the stack
    To use, invoke with:
    raise EndLevel({"state": "status"})
    Code at the higher levels will rely on a dict being passed in to args[0]
    """
    pass
