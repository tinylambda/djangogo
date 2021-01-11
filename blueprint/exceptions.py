class BluePrintException(Exception):
    default_msg = 'BluePrint exception happens'

    def __init__(self, msg=None):
        if msg is None:
            msg = self.default_msg
        self.msg = msg

    def __str__(self):
        return f'BluePrintException<{self.msg}>'


class BluePrintFieldException(BluePrintException):
    def __init__(self, msg=None):
        super(BluePrintFieldException, self).__init__(msg=msg)

    def __str__(self):
        return f'BluePrintFieldException<{self.msg}>'

