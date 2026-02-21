# get_files_info.py
import os
from google.genai import types
from config import MAX_FILE_CHARS

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    List files and subdirectories in the requested directory.
    Only allows access inside the given working_directory (path traversal protection).
    Always returns a string (either formatted listing or error message).
    """
    
    try:
        # Resolve the base directory to absolute path
        working_dir_abs = os.path.abspath(working_directory)

        # Build full target path and normalize it (resolves .. / . / extra slashes etc.)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Security check: target must be contained inside working_dir_abs
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Must be an actual directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Collect entries
        entries = []
        for entry in os.scandir(target_dir):
            try:
                size = entry.stat().st_size
            except (FileNotFoundError, PermissionError):
                size = 0  # fallback in case stat fails

            line = f"- {entry.name}: file_size={size} bytes, is_dir={entry.is_dir()}"
            entries.append(line)

        # Sort for consistent & readable output
        entries.sort()

        if not entries:
            return f"The directory '{directory}' is empty."

        return "\n".join(entries)

    except FileNotFoundError:
        return f'Error: Path "{directory}" does not exist'
    except PermissionError:
        return f'Error: Permission denied when accessing "{directory}"'
    except Exception as e:
        return f'Error: Unexpected error while listing "{directory}": {type(e).__name__}: {str(e)}'