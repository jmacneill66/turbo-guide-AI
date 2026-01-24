from functions.get_file_content import get_file_content
from config import MAX_FILE_CHARS


def test_lorem_truncation():
    content = get_file_content("calculator", "lorem.txt")

    assert not content.startswith("Error:"), "Expected file content, got error"

    assert len(content) > MAX_FILE_CHARS, "Truncation message missing"

    assert f'truncated at {MAX_FILE_CHARS} characters' in content, (
        "Expected truncation message not found"
    )

    print("✔ lorem.txt truncation test passed")
    print(f"Returned length: {len(content)}")


def run_other_tests():
    print("\n--- Additional test cases ---\n")

    tests = [
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py"),
    ]

    for working_dir, path in tests:
        print(f"Test: get_file_content({working_dir!r}, {path!r})")
        result = get_file_content(working_dir, path)
        print(result)  # avoid dumping large files
        print("-" * 60)


if __name__ == "__main__":
    test_lorem_truncation()
    run_other_tests()
