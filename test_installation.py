#!/usr/bin/env python3
"""
Installation Test Script
Verifies that all dependencies are installed correctly
"""

import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing Python installation...\n")

    tests = [
        ("Python version", lambda: sys.version_info >= (3, 7), f"Python {sys.version}"),
        ("requests", lambda: __import__('requests'), None),
        ("beautifulsoup4", lambda: __import__('bs4'), None),
        ("flask", lambda: __import__('flask'), None),
        ("lxml", lambda: __import__('lxml'), None),
    ]

    all_passed = True

    for test_name, test_func, extra_info in tests:
        try:
            result = test_func()
            if result or result is None:
                status = "✓"
                message = "PASS"
                if extra_info:
                    message += f" - {extra_info}"
            else:
                status = "✗"
                message = "FAIL"
                all_passed = False
        except Exception as e:
            status = "✗"
            message = f"FAIL - {str(e)}"
            all_passed = False

        print(f"{status} {test_name:20s} {message}")

    return all_passed


def test_modules():
    """Test if custom modules can be imported"""
    print("\nTesting custom modules...\n")

    modules = [
        "scraper",
        "downloader",
    ]

    all_passed = True

    for module_name in modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name:20s} OK")
        except Exception as e:
            print(f"✗ {module_name:20s} FAIL - {str(e)}")
            all_passed = False

    return all_passed


def main():
    """Run all tests"""
    print("=" * 60)
    print("Universal Web Scraper & Downloader - Installation Test")
    print("=" * 60)
    print()

    deps_ok = test_imports()
    modules_ok = test_modules()

    print()
    print("=" * 60)

    if deps_ok and modules_ok:
        print("✓ All tests passed! Installation is successful.")
        print()
        print("You can now run the app:")
        print("  • Web interface: python app.py")
        print("  • CLI interface: python main.py")
        print("  • Quick start:   ./quickstart.sh (or quickstart.bat on Windows)")
    else:
        print("✗ Some tests failed. Please install missing dependencies:")
        print("  pip install -r requirements.txt")

    print("=" * 60)


if __name__ == "__main__":
    main()
