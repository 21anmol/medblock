from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Serve static files from the frontend directory
@app.route('/')
def serve_index():
    return send_from_directory('medblock/frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('medblock/frontend', path)

@app.route('/test')
def test():
    return 'MedBlock Test Server is Running!'

if __name__ == '__main__':
    print("Server starting at http://localhost:7000")
    app.run(host='localhost', port=7000, debug=True) 