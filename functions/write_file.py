import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file inside the permitted working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)
   
def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Write string content to a file inside the permitted working_directory.
    Creates parent directories if needed.
    Returns status message (success or error string).
    """
    try:
        # Resolve base directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize full target path
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Path traversal protection
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" — path is outside the permitted working directory'

        # Prevent overwriting a directory
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" — it is a directory'

        # Get the parent directory of the target file
        parent_dir = os.path.dirname(target_path)

        # Create parent directories if they don't exist
        if parent_dir and not os.path.isdir(parent_dir):
            try:
                os.makedirs(parent_dir, exist_ok=True)
            except Exception as e:
                return f'Error: Failed to create parent directories for "{file_path}": {type(e).__name__}: {str(e)}'

        # Optional: size limit (adjust as needed)
        MAX_CONTENT_LENGTH = 10_000_000  # 10 MB
        if len(content) > MAX_CONTENT_LENGTH:
            return f'Error: Content too large ({len(content):,} characters). Max allowed: {MAX_CONTENT_LENGTH:,}'

        # Write the file (UTF-8 by default)
        try:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content):,} characters written)'
            
        except UnicodeEncodeError:
            return f'Error: Content contains characters that cannot be encoded in UTF-8'

    except FileNotFoundError:
        return f'Error: Parent path component does not exist and could not be created for "{file_path}"'
    except PermissionError:
        return f'Error: Permission denied when writing to "{file_path}"'
    except OSError as e:
        return f'Error: OS error while writing "{file_path}": {type(e).__name__}: {str(e)}'
    except Exception as e:
        return f'Error: Unexpected error writing "{file_path}": {type(e).__name__}: {str(e)}'