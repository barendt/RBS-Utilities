class RBSError(Exception):
    """Generic exception to use for flow control.

    """
    def __init__(self, msg):
        self.msg = msg
