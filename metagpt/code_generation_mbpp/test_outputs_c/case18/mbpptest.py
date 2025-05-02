from remove_string import CharRemover
# "test_list": ["assert remove_dirty_chars(\"probasscurve\", \"pros\") == 'bacuve'", "assert remove_dirty_chars(\"digitalindia\", \"talent\") == 'digiidi'", "assert remove_dirty_chars(\"exoticmiles\", \"toxic\") == 'emles' "
    
def test_remove_dirty_chars():
    if CharRemover.remove_chars("probasscurve", "pros") == 'bacuve':
        print("Test passed")
    if CharRemover.remove_chars("digitalindia", "talent") == 'digiidi':
        print("Test passed")
    if CharRemover.remove_chars("exoticmiles", "toxic") == 'emles':
        print("Test passed")

test_remove_dirty_chars()