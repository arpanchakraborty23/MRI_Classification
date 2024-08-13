import logging
import os
from pathlib import Path

list_of_files=[
    'config/config.yaml',
    'params.yaml',
    'data',
    '.github/.gitkeep',
    'src/__init__.py',
    'src/components/__init__.py',
    'src/constant/__init__.py',
    'src/configure/__init__.py', 
    'src/entity/__init__.py',
    'src/logger/__init__.py',
    'src/exception/__init__.py', 
    'src/utils/__init__.py',
    'src/pipeline/__init__.py',
    'README.md',
    'templates/index.html',
    'app.py',
    'requirements.txt',
    'setup.py'
]

for filepath in list_of_files:
    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    
    if(not os.path.exists(filename)) or (os.path.getsize(filename) == 0):
        with open(filepath, 'w') as f:
            pass
            logging.info(f"Creating empty file: {filename}")

    
    else:
        logging.info(f"{filename} is already created")