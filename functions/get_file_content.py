import os
from google.genai import types
from config import MAX_FILE_CHARS


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file, with truncation if it exceeds the maximum character limit",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Provides file contents for a given file path relative to the working directory",
            ),
        
        },
    ),
)

def get_file_content(working_directory: str, file_path: str = ".") -> str:
    """
    Read and return the content of a file as a string.
    Only allows reading files inside the given working_directory.
    Always returns a string (either file content or error message).
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            if os.path.isdir(target_path):
                return f'Error: "{file_path}" is a directory, not a file'
            return f'Error: "{file_path}" does not exist or is not a regular file'

        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_FILE_CHARS)

            # Check for truncation
            if f.read(1):
                content += (
                    f'\n\n[...File "{file_path}" truncated at '
                    f'{MAX_FILE_CHARS} characters]'
                )

        return content

    except UnicodeDecodeError:
        return f'Error: Cannot read "{file_path}" as text (non-UTF-8 or binary file)'
    except Exception as e:
        return f'Error: {type(e).__name__}: {e}'
