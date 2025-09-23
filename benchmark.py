import time
import importlib
import sys
from typing import Callable, Dict, List, Any, Tuple, Optional

def benchmark_function(func: Callable, args: Tuple = (), kwargs: Dict = {}, 
                      runs: int = 5) -> Dict[str, Any]:
    """
    Run a function multiple times and calculate average execution time.
    
    Parameters:
    -----------
    func : Callable
        The function to benchmark
    args : Tuple
        Positional arguments to pass to the function
    kwargs : Dict
        Keyword arguments to pass to the function
    runs : int
        Number of times to run the function
        
    Returns:
    --------
    Dict[str, Any]
        Dictionary containing benchmark results
    """
    times = []
    results = []
    
    print(f"Benchmarking {func.__name__}...")
    
    for i in range(runs):
        print(f"  Run {i+1}/{runs}", end="... ")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        times.append(execution_time)
        results.append(result)
        print(f"completed in {execution_time:.5f} ms")
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"\nResults for {func.__name__}:")
    print(f"  Average time: {avg_time:.5f} ms")
    print(f"  Min time: {min_time:.5f} ms")
    print(f"  Max time: {max_time:.5f} ms")
    print(f"  Total runs: {runs}")
    
    return {
        "function": func.__name__,
        "average_time": avg_time,
        "min_time": min_time,
        "max_time": max_time,
        "times": times,
        "results": results,
        "runs": runs
    }

def import_function(module_name: str, function_name: str) -> Optional[Callable]:
    """
    Import a function from a module
    
    Parameters:
    -----------
    module_name : str
        Name of the module to import from
    function_name : str
        Name of the function to import
        
    Returns:
    --------
    Callable or None
        The imported function or None if import fails
    """
    try:
        module = importlib.import_module(module_name)
        return getattr(module, function_name)
    except (ImportError, AttributeError) as e:
        print(f"Error importing {function_name} from {module_name}: {e}")
        return None

def benchmark_prime_generation(bit_sizes: List[int] = [32, 64, 128], runs: int = 5):
    """
    Benchmark prime number generation with different bit sizes
    """
    from prime_number_generation import generate_large_prime
    
    results = {}
    
    for bits in bit_sizes:
        print(f"\n=== Benchmarking generate_large_prime with {bits} bits ===")
        result = benchmark_function(generate_large_prime, args=(bits,), runs=runs)
        results[f"generate_large_prime_{bits}bits"] = result
    
    return results

def benchmark_key_generation(bit_sizes: List[int] = [32, 64, 128], runs: int = 5):
    """
    Benchmark RSA key generation with different bit sizes
    """
    try:
        from generate_keypair import generate_key_pairs
        
        results = {}
        
        for bits in bit_sizes:
            print(f"\n=== Benchmarking generate_key_pairs with {bits} bits ===")
            result = benchmark_function(generate_key_pairs, args=(bits,), runs=runs)
            results[f"generate_key_pairs_{bits}bits"] = result
        
        return results
    except ImportError:
        print("Could not import generate_keypair function")
        return {}

def benchmark_custom_function(module_name: str, function_name: str, 
                             args: Tuple = (), kwargs: Dict = {}, runs: int = 5):
    """
    Benchmark a custom function
    
    Parameters:
    -----------
    module_name : str
        Name of the module containing the function
    function_name : str
        Name of the function to benchmark
    args : Tuple
        Positional arguments to pass to the function
    kwargs : Dict
        Keyword arguments to pass to the function
    runs : int
        Number of times to run the function
    """
    func = import_function(module_name, function_name)
    if func:
        return benchmark_function(func, args=args, kwargs=kwargs, runs=runs)
    return None

def main():
    """
    Main function to run benchmarks
    """
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python benchmark.py prime [runs] [bit_sizes]")
        print("  python benchmark.py keypair [runs] [bit_sizes]")
        print("  python benchmark.py custom <module_name> <function_name> [runs] [arg1,arg2,...]")
        print("\nExamples:")
        print("  python benchmark.py prime 5 32,64,128")
        print("  python benchmark.py keypair 3 64,128")
        print("  python benchmark.py custom prime_number_generation fermat 10")
        return
    
    benchmark_type = sys.argv[1].lower()
    
    # Default number of runs
    runs = 5
    if len(sys.argv) > 2 and sys.argv[2].isdigit():
        runs = int(sys.argv[2])
    
    if benchmark_type == "prime":
        # Default bit sizes
        bit_sizes = [32, 64, 128]
        if len(sys.argv) > 3:
            try:
                bit_sizes = [int(b) for b in sys.argv[3].split(",")]
            except ValueError:
                print(f"Invalid bit sizes: {sys.argv[3]}")
                print("Using default bit sizes: 32, 64, 128")
        
        benchmark_prime_generation(bit_sizes=bit_sizes, runs=runs)
    
    elif benchmark_type == "keypair":
        # Default bit sizes
        bit_sizes = [32, 64, 128]
        if len(sys.argv) > 3:
            try:
                bit_sizes = [int(b) for b in sys.argv[3].split(",")]
            except ValueError:
                print(f"Invalid bit sizes: {sys.argv[3]}")
                print("Using default bit sizes: 32, 64, 128")
        
        benchmark_key_generation(bit_sizes=bit_sizes, runs=runs)
    
    elif benchmark_type == "custom":
        if len(sys.argv) < 4:
            print("For custom benchmarks, please provide module name and function name:")
            print("  python benchmark.py custom <module_name> <function_name> [runs]")
            return
        
        module_name = sys.argv[2]
        function_name = sys.argv[3]
        
        # Custom number of runs if provided
        run_arg_index = 4
        if len(sys.argv) > run_arg_index and sys.argv[run_arg_index].isdigit():
            runs = int(sys.argv[run_arg_index])
            run_arg_index += 1
        
        # Handle custom arguments if provided
        args = ()
        if len(sys.argv) > run_arg_index:
            # Try to parse arguments - simple version just assumes all are integers
            try:
                args = tuple(int(arg) for arg in sys.argv[run_arg_index].split(","))
                print(f"Using arguments: {args}")
            except ValueError:
                print(f"Could not parse arguments: {sys.argv[run_arg_index]}")
                print("Proceeding without arguments")
        
        benchmark_custom_function(module_name, function_name, args=args, runs=runs)
    
    else:
        print(f"Unknown benchmark type: {benchmark_type}")
        print("Available types: prime, keypair, custom")

if __name__ == "__main__":
    main()