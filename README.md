# Complexity Visualizer API
A Flask API to analyze and visualize algorithm time complexity.

Features

	* Analyze bubble sort, linear search, binary search, and nested loops
	* Returns JSON with execution times and base64-encoded graph
	* Real-time complexity visualization

Installation
# Clone the repository
git clone https://github.com/waka-man/complexity_visualizer.git
cd complexity_visualizer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

Usage
# Run the Flask app
python3 app.py

The API will be available at http://localhost:3000

API Endpoints
GET /
Returns API information and available algorithms.

GET /analyze
Analyzes algorithm complexity.

Query Parameters:

	* algo - Algorithm name (bubble, linear, binary, nested, exponential)
	* n - Maximum input size (default: 1000)
	* steps - Step size (default: 10)

Example:

http://localhost:3000/analyze?algo=bubble&n=1000&steps=10

Response:

{
  "algorithm": "bubble",
  "parameters": {
    "n": 1000,
    "steps": 10,
    "n_min": 10,
    "n_max": 1000
  },
  "analysis": {
    "input_sizes": [10, 20, 30, ...],
    "execution_times": [0.0001, 0.0004, ...],
    "total_analysis_time": 2.5432
  },
  "graph": {
    "format": "png",
    "encoding": "base64",
    "data": "iVBORw0KGgoAAAANSUhEUg..."
  }
}

Available Algorithms
	* bubble - Bubble Sort (O(n²))
	* linear - Linear Search (O(n))
	* binary - Binary Search (O(log n))
	* nested - Nested Loops (O(n²))
	* exponential - Nested Loops (O(n²))

Requirements
	* Python 3.x
	* Flask
	* NumPy
	* Matplotlib
