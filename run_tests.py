#!/usr/bin/env python3
"""
Simple test runner for Advanced Terminal Chatbot.
"""

import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    try:
        import pytest
        
        # Run tests with coverage
        print("🧪 Running tests with coverage...")
        exit_code = pytest.main([
            "tests/",
            "--cov=src",
            "--cov-report=term-missing",
            "--cov-report=html",
            "-v"
        ])
        
        if exit_code == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Some tests failed (exit code: {exit_code})")
        
        sys.exit(exit_code)
        
    except ImportError:
        print("❌ pytest not found. Please install it first:")
        print("   pip install pytest pytest-cov")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        sys.exit(1)
