import os
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# Define source directory
source_dir = '/root'

# Automatically determine the destination directory within the current working directory
current_working_directory = os.getcwd()
destination_dir = os.path.join(current_working_directory, 'copied_files')

# Ensure destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Copy files from source to destination
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # Create the same directory structure in the destination directory
        dest_dir_path = os.path.join(destination_dir, os.path.relpath(root, source_dir))
        os.makedirs(dest_dir_path, exist_ok=True)
        shutil.copy(os.path.join(root, file), dest_dir_path)

# Function to start a simple HTTP server
def start_server(directory, port=8000):
    os.chdir(directory)
    httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    httpd.serve_forever()

# Start the HTTP server in a separate thread
server_thread = threading.Thread(target=start_server, args=(destination_dir,))
server_thread.daemon = True
server_thread.start()

print(f"Files copied to {destination_dir} and available for download at http://localhost:8000")