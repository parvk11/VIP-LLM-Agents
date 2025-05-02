class CharRemover:
    @staticmethod
    def remove_chars(s1: str, s2: str) -> str:
        s1_set = set(s1)
        s2_set = set(s2)
        result = ''.join(char for char in s1 if char not in s2_set)
        return result
