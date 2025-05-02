class CharRemover:
    def remove_chars(s1: str, s2: str) -> str:
        """
        Removes characters from s1 based on s2 and returns the modified string.

        Args:
        s1: The original string from which characters will be removed.
        s2: The string containing the characters to be removed from s1.

        Returns:
        The modified string after removing characters based on s2.
        """
        if not s2:
            return s1
        else:
            return ''.join([char for char in s1 if char not in s2])
