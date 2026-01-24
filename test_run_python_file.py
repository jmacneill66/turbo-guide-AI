from functions.run_python_file import run_python_file

def run_all_tests():
    tests = [
        ("calculator", "main.py", None, "Calculator usage instructions"),
        ("calculator", "main.py", ["3 + 5"], "Run calculator with input"),
        ("calculator", "tests.py", None, "Run calculator's tests"),
        ("calculator", "../main.py", None, "Path traversal blocked"),
        ("calculator", "nonexistent.py", None, "File does not exist"),
        ("calculator", "lorem.txt", None, "Not a Python file"),
    ]

    for working_dir, file_path, args, description in tests:
        print(f"\n--- Test: {description} ---")
        result = run_python_file(working_dir, file_path, args)
        print(result)
        print("-" * 60)

if __name__ == "__main__":
    run_all_tests()
