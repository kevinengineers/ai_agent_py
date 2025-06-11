import os


def get_file_content(working_dir, file_path):
    try:
        # get abs path of working_dir
        work_dir_abs = os.path.abspath(working_dir)

        # get abs filepath and verify file_path lives inside working dir.
        file_path_abs = os.path.abspath(os.path.join(work_dir_abs, file_path))
        valid_dir = file_path_abs.startswith(work_dir_abs)

        # check if it's a valid file.
        is_valid_file = os.path.isfile(file_path_abs)
    except Exception as e:
        return f"Error: {e}"
    # set char length of text we will pass to the AI model
    MAX_CHARS = 10000

    # if a file is not inside our working directory or is not a valid filename
    if not valid_dir:
        return f'Error: Cannot read "{
            file_path
        }" as it is outside the permitted working directory'
    elif not is_valid_file:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        try:
            with open(file_path_abs, "r") as f:
                file_content_str = f.read(MAX_CHARS)
                return file_content_str
        except Exception as e:
            return f"Error: {e}"
