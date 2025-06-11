import os 
 
def get_files_info(working_directory, directory=None):
    try:
        work_dir_abs = os.path.abspath(working_directory)
        dir_abs = os.path.abspath(os.path.join(working_directory, directory))

        if not dir_abs.startswith(work_dir_abs):
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        elif not os.path.isdir(dir_abs):
            return f"Error: \"{directory}\" is not a directory"
        else:

            dir_as_list = os.listdir(dir_abs)
            file_info_list = []

            for item in dir_as_list:
                file_name = item
                file_size = os.path.getsize(os.path.join(dir_abs, item))
                file_is_dir = os.path.isdir(os.path.join(dir_abs, item))
                item = f"- {file_name}: file_size={file_size} bytes, is_dir={file_is_dir}"
                file_info_list.append(item)

            file_info_str = "\n".join(file_info_list)
            return file_info_str
    except Exception as error:
        return f"Error: {error}"
