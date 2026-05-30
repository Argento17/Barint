"""
Pytest fixtures available across all tests.
"""
import sys
import os

# Make sure tests can import from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))