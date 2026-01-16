import zipfile
import os

# Create a zip file named 'processing.zip'
with zipfile.ZipFile('processing.zip', 'w') as zf:
    # Add the processing.py file to the zip
    # 'arcname' ensures it sits at the root of the zip, not inside folders
    zf.write('src/lambda/processing.py', arcname='processing.py')

# Check the size
size = os.path.getsize('processing.zip')
print(f"✅ Success! Created processing.zip. File size: {size} bytes")