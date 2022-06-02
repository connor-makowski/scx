import sys


class Error:
    @classmethod
    def warn(self, message, depth=0):
        """
        Usage:

        - Creates a class based warning message

        Requires:

        - `message`:
            - Type: str
            - What: The message to warn users with

        Optional:

        - `depth`:
            - Type: int
            - What: The depth of the nth call below the top of the method stack
            - Note: Depth starts at 0 (indicating the current method in the stack)
            - Default: 0
        """
        print(
            f"(Warning for `{self.__class__.__name__}.{sys._getframe(depth).f_back.f_code.co_name}`): {message}"
        )

    @classmethod
    def exception(self, message, depth=0):
        """
        Usage:
        - Creates a class based exception message
        Requires:
        - `message`:
            - Type: str
            - What: The message to raise an exception with
        Optional:

        - `depth`:
            - Type: int
            - What: The depth of the nth call below the top of the method stack
            - Note: Depth starts at 0 (indicating the current method in the stack)
            - Default: 0
        """
        raise Exception(
            f"(`{self.__class__.__name__}.{sys._getframe(depth).f_back.f_code.co_name}`): {message}"
        )
