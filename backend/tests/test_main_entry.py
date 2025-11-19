"""
Test to cover the main entry point (if __name__ == "__main__")
This test file uses runpy to execute main.py as __main__
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import runpy


class TestMainEntry:
    """Test main.py entry point execution"""

    def test_main_module_can_run_as_script(self):
        """Test that main.py can be run as __main__ (covers lines 66-67)"""
        # Get the path to main.py
        main_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'main.py'
        )

        # Mock uvicorn.run to prevent actual server start
        with patch('uvicorn.run') as mock_uvicorn_run:
            # Use runpy to execute main.py as if it's __main__
            # This properly triggers coverage for the if __name__ == "__main__" block
            try:
                runpy.run_path(main_file, run_name='__main__')
            except SystemExit:
                # runpy or uvicorn might call sys.exit, that's expected
                pass

            # Verify uvicorn.run was called
            assert mock_uvicorn_run.called, "uvicorn.run should have been called when running as __main__"

            # Verify it was called with correct parameters
            call_args = mock_uvicorn_run.call_args
            assert call_args is not None, "uvicorn.run should have received arguments"

            # The first argument should be the app string
            args = call_args[0] if call_args[0] else []
            kwargs = call_args[1] if len(call_args) > 1 else {}

            # Verify key parameters
            if args:
                assert "main:app" in str(args[0]), f"Expected 'main:app', got {args[0]}"
            assert kwargs.get('host') == "0.0.0.0", f"Expected host='0.0.0.0', got {kwargs.get('host')}"
            assert kwargs.get('port') == 8000, f"Expected port=8000, got {kwargs.get('port')}"
