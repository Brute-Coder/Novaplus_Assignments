import os
import sys

def create_project_structure():
    """Create the project directory structure"""
    # Define the directory structure
    directories = [
        'src',
        'data',
        'models',
    ]
    
    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create __init__.py in src directory
    with open(os.path.join('src', '__init__.py'), 'w') as f:
        pass
    
    # Create README.md with basic project information
    readme_content = """# Cryptocurrency Price Prediction System

A machine learning system for predicting cryptocurrency price movements using LSTM networks.

## Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate virtual environment:
   - Windows: `venv\\Scripts\\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Start the GUI:
   ```bash
   streamlit run src/app.py
   ```

## Project Structure
- `src/`: Source code
- `data/`: Data storage
- `models/`: Trained models
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)

    print("Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()