from remove_string import CharRemover
def test_remove_chars():
    assert CharRemover.remove_chars("hello", "world") == "he"
    assert CharRemover.remove_chars("python", "java") == "python"
    assert CharRemover.remove_chars("abc", "def") == "abc"

test_remove_chars()