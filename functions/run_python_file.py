import os
import subprocess


def run_python_file(work_dir, file_path):
    abs_work_dir = os.path.abspath(work_dir)
    abs_file_path = os.path.abspath(os.path.join(abs_work_dir, file_path))
    root, ext = os.path.splitext(file_path)
    if not abs_file_path.startswith(abs_work_dir):
        return (
            f'Error: Cannot execute "{
                file_path
                }" as it is outside the permitted working directory'
        )
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if ext != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(
            ["python3", abs_file_path],
            timeout=30,
            capture_output=True
        )
        std_out = result.stdout.decode()
        std_err = result.stderr.decode()
        user_output = ""
        user_output += f"STDOUT: {std_out.strip()}\n"
        user_output += f"STDERR: {std_err.strip()}\n"
        if len(std_out) == 0 and len(std_err) == 0:
            return "No output produced."
        if result.returncode != 0:
            user_output += f"Process exited with code {result.returncode}\n"
        return user_output
    except Exception as e:
        return f"Error: executing Python file {e}"
