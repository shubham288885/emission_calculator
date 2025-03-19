import os
import sys
import subprocess
import traceback

def run_streamlit():
    """
    Run the Streamlit app with proper environment setup and error reporting.
    """
    try:
        # Print current directory for debugging
        current_dir = os.path.abspath(os.path.dirname(__file__))
        print(f"Current directory: {current_dir}")
        
        # The app is in the multimodal_data_extractor subdirectory
        app_dir = os.path.join(current_dir, 'multimodal_data_extractor')
        print(f"App directory: {app_dir}")
        
        # Set PYTHONPATH to app directory *first* in sys.path to avoid conflicts
        # This helps avoid package naming conflicts
        os.environ['PYTHONPATH'] = app_dir
        sys.path.insert(0, app_dir)  # Ensure app directory is first in path
        print(f"PYTHONPATH set to: {os.environ.get('PYTHONPATH')}")
        
        # Check if the target file exists
        streamlit_app_path = os.path.join(app_dir, 'app', 'frontend', 'streamlit_app.py')
        if not os.path.exists(streamlit_app_path):
            print(f"ERROR: Streamlit app not found at {streamlit_app_path}")
            return
        
        print(f"Found Streamlit app at: {streamlit_app_path}")
        
        # Verify PyMuPDF is properly installed
        try:
            import fitz
            print(f"PyMuPDF (fitz) version: {fitz.__version__}")
            # Make sure it's the right PyMuPDF, not a conflicting package
            if not hasattr(fitz, 'open'):
                print("WARNING: PyMuPDF seems to be incorrectly installed!")
                install_pymupdf()
        except ImportError:
            print("PyMuPDF (fitz) is not installed. Installing now...")
            install_pymupdf()
        except Exception as e:
            print(f"Warning with PyMuPDF import: {str(e)}")
            install_pymupdf()
            
        # Check for other required dependencies
        try:
            import streamlit
            import numpy
            import cv2
            print("All core dependencies verified!")
        except ImportError as e:
            print(f"ERROR: Missing dependency: {e}")
            print("Please run: pip install streamlit numpy opencv-python")
            return
        
        # Create __init__.py files to help with imports
        init_script_path = os.path.join(app_dir, 'create_init_files.py')
        if os.path.exists(init_script_path):
            print("Running init file creator script...")
            subprocess.call([sys.executable, init_script_path])
        
        # Run Streamlit
        print("\n--- Starting Streamlit App ---")
        print(f"App will be available at: http://localhost:8501")
        print("Press Ctrl+C to stop the app")
        print("-------------------------------\n")
        
        # Change to app directory before running
        os.chdir(app_dir)
        
        # Use subprocess to run streamlit with a clean environment
        env = os.environ.copy()
        env["PYTHONPATH"] = app_dir  # Ensure PYTHONPATH is set in subprocess
        
        cmd = [sys.executable, "-m", "streamlit", "run", "app/frontend/streamlit_app.py"]
        subprocess.call(cmd, env=env)
        
    except Exception as e:
        print(f"ERROR: Failed to start Streamlit app: {e}")
        print("\nTraceback:")
        traceback.print_exc()

def install_pymupdf():
    """Install PyMuPDF correctly."""
    print("Installing PyMuPDF 1.25.1...")
    subprocess.call([sys.executable, "-m", "pip", "uninstall", "-y", "frontend", "PyMuPDF"])
    subprocess.call([sys.executable, "-m", "pip", "install", "pymupdf==1.25.1"])
    print("PyMuPDF installation completed.")

if __name__ == "__main__":
    run_streamlit() 