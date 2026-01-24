import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file inside the permitted working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Arguments to pass to the Python file",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    """
    Run a Python file safely inside working_directory with optional args.
    Returns a string describing the output, errors, and exit code.
    """

    try:
        # Resolve absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Security check: must stay inside working directory
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Must be a regular file
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Must be a Python file
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        cmd = ["python", target_path]
        if args:
            cmd.extend(args)  # use extend as requested

        # Run the command with a timeout
        completed = subprocess.run(
            cmd,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,  # decode bytes to str
            timeout=30  # prevent infinite execution
        )

        # Build output string
        output_parts = []

        if completed.returncode != 0:
            output_parts.append(f"Process exited with code {completed.returncode}")

        if not completed.stdout and not completed.stderr:
            output_parts.append("No output produced")
        else:
            if completed.stdout:
                output_parts.append(f"STDOUT:\n{completed.stdout}")
            if completed.stderr:
                output_parts.append(f"STDERR:\n{completed.stderr}")

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return f"Error: executing Python file: timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {type(e).__name__}: {str(e)}"
