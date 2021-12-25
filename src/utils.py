import string
import random


class Utils():
    @staticmethod
    def random_string(length: int) -> str:
        """
        returns a random lowercase letter string with the provided length.
        """
        letters = string.ascii_lowercase
        result = "".join(random.choice(letters) for _ in range(length))
        return result
