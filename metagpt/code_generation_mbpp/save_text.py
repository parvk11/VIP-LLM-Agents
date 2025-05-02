import os
def save_text_to_file(name, text, path_provided):
    full_path = ""
    if path_provided:
        full_path = name
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # dir where script lives
        directory = os.path.join(base_dir, "test_outputs_c")
        full_path = os.path.join(directory, name)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, 'w') as file:
        file.write(text)

    print(f"Text saved to {full_path}")