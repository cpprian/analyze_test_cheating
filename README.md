# How to install conda env for this project
conda create -n eye_detection python=3.9 numpy  
  
conda activate eye_detection 
  
conda install -c conda-forge opencv  
conda install -c conda-forge pynput 
conda install -c conda-forge dlib  
pip install --upgrade pyobjc==7.3 