
import os


def write_file(working_dir, file_path, content):
    work_dir_abs = os.path.abspath(working_dir)
    file_path_abs = os.path.abspath(os.path.join(work_dir_abs, file_path))
    valid_file_path = file_path_abs.startswith(work_dir_abs)
    if not valid_file_path:
        return f'Error: Cannot write to "{
            file_path
            }" as it is outside the permitted working directory'
    if not os.path.exists(file_path_abs):
        try:
            os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(file_path_abs) and os.path.isdir(file_path_abs):
        return f'Error: "{file_path} is a directory, not a file'
    try:
        with open(file_path_abs, "w") as f:
            f.write(content)
        return f"Successfully wrote to '{
            file_path
            } ({len(content)} characters written)"
    except Exception as e:
        return f"Error: writing to file {e}"
