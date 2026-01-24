#!/usr/bin/env python3
"""
Manual test / debug helper for get_files_info()
Run with: uv run test_get_files_info.py
"""

from functions.get_files_info import get_files_info


def show_result(label: str, dir_arg: str) -> None:
    print(f"\nget_files_info(\"calculator\", {dir_arg!r}):")
    print(f"Result for {label}:")
    result = get_files_info("calculator", dir_arg)
    for line in result.splitlines():
        print(f"  {line}")


def main():
    cases = [
        (".",          "current directory"),
        ("pkg",        "'pkg' directory"),
        ("/bin",       "'/bin' directory"),
        ("../",        "'../' directory"),
        ("pkg/..",     "pkg/.. (should still be blocked)"),
        ("nonexistent", "non-existent folder"),
    ]

    for dir_arg, label in cases:
        show_result(label, dir_arg)


if __name__ == "__main__":
    main()