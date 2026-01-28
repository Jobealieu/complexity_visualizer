from flask import Flask, request, jsonify
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Algorithm implementations
def linear_search(n):
    for i in range(n):
        if i == n-1:
            return i

def bubble_sort(n):
    arr = np.random.randint(0, 100, n)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def binary_search(n):
    arr = sorted(np.random.randint(0, 100, n))
    target = arr[-1]
    left, right = 0, n - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def nested_loops(n):
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
    return count

# Algorithm mapper
ALGORITHMS = {
    'bubble': bubble_sort,
    'linear': linear_search,
    'binary': binary_search,
    'nested': nested_loops,
    'exponential': nested_loops  # alias
}

def time_complexity_visualizer(algorithm, n_min, n_max, n_step):
    times = []
    input_sizes = list(range(n_min, n_max + n_step, n_step))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Input size')
    ax.set_ylabel('Running time (seconds)')
    ax.set_title(f'Algorithm time complexity visualization')
    
    for n in input_sizes:
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)
    
    ax.plot(input_sizes, times, 'o-', linewidth=2, markersize=6)
    ax.grid(True, alpha=0.3)
    
    # Convert plot to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    
    return times, input_sizes, img_base64

@app.route('/analyze', methods=['GET'])
def analyze():
    try:
        # Get query parameters
        algo_name = request.args.get('algo', 'bubble').lower()
        n = int(request.args.get('n', 1000))
        steps = int(request.args.get('steps', 10))
        
        # Validate algorithm
        if algo_name not in ALGORITHMS:
            return jsonify({
                'error': f'Invalid algorithm. Choose from: {", ".join(ALGORITHMS.keys())}'
            }), 400
        
        # Get the algorithm function
        algorithm = ALGORITHMS[algo_name]
        
        # Calculate n_min and n_max
        n_min = max(10, steps)
        n_max = n
        n_step = steps
        
        # Run analysis and measure total time
        total_start = time.time()
        times, input_sizes, img_base64 = time_complexity_visualizer(
            algorithm, n_min, n_max, n_step
        )
        total_time = time.time() - total_start
        
        # Format response
        response = {
            'algorithm': algo_name,
            'parameters': {
                'n': n,
                'steps': steps,
                'n_min': n_min,
                'n_max': n_max
            },
            'analysis': {
                'input_sizes': input_sizes,
                'execution_times': times,
                'total_analysis_time': round(total_time, 4)
            },
            'graph': {
                'format': 'png',
                'encoding': 'base64',
                'data': img_base64
            }
        }
        
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid parameter value: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Complexity Visualizer API',
        'endpoints': {
            '/analyze': 'Analyze algorithm complexity',
        },
        'example': '/analyze?algo=bubble&n=1000&steps=10',
        'available_algorithms': list(ALGORITHMS.keys())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
