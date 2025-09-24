#!/usr/bin/env python3

import argparse
from prime_number_generation import fermat, miller_rabin
from collections import defaultdict
import matplotlib.pyplot as plt

# Some well-known Carmichael numbers (composite numbers that can fool Fermat test)
CARMICHAEL_NUMBERS = [
    561,    # 3 * 11 * 17
    1105,   # 5 * 13 * 17
    1729,   # 7 * 13 * 19
    2465,   # 5 * 17 * 29
    2821,   # 7 * 13 * 31
    6601,   # 7 * 23 * 41
    8911,   # 7 * 19 * 67
]

def test_primality_iterations(number, max_k=100, trials=100):
    """
    Test a number with both Fermat and Miller-Rabin for multiple values of k and trials
    Returns the false positive rates for each k value
    """
    fermat_false_positives = defaultdict(int)
    miller_rabin_false_positives = defaultdict(int)
    
    # Test with different k values
    for k in range(1, max_k + 1):
        # Run multiple trials for each k to account for randomness
        for _ in range(trials):
            fermat_result = fermat(number, k)
            miller_rabin_result = miller_rabin(number, k)
            
            # For composite numbers, a "True" result is a false positive
            if fermat_result:  # If Fermat says it's prime (which is wrong for Carmichael)
                fermat_false_positives[k] += 1
            
            if miller_rabin_result:  # If Miller-Rabin says it's prime (which is wrong)
                miller_rabin_false_positives[k] += 1
    
    # Convert to probabilities
    fermat_probs = {k: count/trials for k, count in fermat_false_positives.items()}
    miller_rabin_probs = {k: count/trials for k, count in miller_rabin_false_positives.items()}
    
    return fermat_probs, miller_rabin_probs

def plot_results(number, fermat_probs, miller_rabin_probs):
    """Plot the false positive rates for both algorithms"""
    plt.figure(figsize=(10, 6))
    
    # Convert the dictionaries to lists for plotting
    ks = sorted(list(set(list(fermat_probs.keys()) + list(miller_rabin_probs.keys()))))
    fermat_rates = [fermat_probs.get(k, 0) for k in ks]
    miller_rabin_rates = [miller_rabin_probs.get(k, 0) for k in ks]
    
    plt.plot(ks, fermat_rates, 'r-', label='Fermat Test')
    plt.plot(ks, miller_rabin_rates, 'b-', label='Miller-Rabin Test')
    
    plt.title(f'False Positive Rates for Primality Tests on {number}')
    plt.xlabel('k (number of iterations)')
    plt.ylabel('Probability of False Positive')
    plt.legend()
    plt.grid(True)
    
    # Save the figure
    plt.savefig(f'carmichael_{number}_comparison.png')
    plt.close()
    
    return f'carmichael_{number}_comparison.png'

def main():
    parser = argparse.ArgumentParser(description='Test primality tests on Carmichael numbers')
    parser.add_argument('--number', type=int, choices=CARMICHAEL_NUMBERS, 
                        default=561, help='Carmichael number to test')
    parser.add_argument('--max-k', type=int, default=20, 
                        help='Maximum number of iterations (k) to test')
    parser.add_argument('--trials', type=int, default=100, 
                        help='Number of trials for each k')
    args = parser.parse_args()
    
    print(f"Testing Carmichael number {args.number} with up to k={args.max_k} iterations")
    print(f"Running {args.trials} trials per k value")
    
    fermat_probs, miller_rabin_probs = test_primality_iterations(
        args.number, args.max_k, args.trials
    )
    
    print("\nFermat Test False Positive Rates:")
    for k in sorted(fermat_probs.keys()):
        print(f"  k={k}: {fermat_probs[k]:.4f}")
    
    print("\nMiller-Rabin Test False Positive Rates:")
    for k in sorted(miller_rabin_probs.keys()):
        print(f"  k={k}: {miller_rabin_probs[k]:.4f}")
    
    plot_file = plot_results(args.number, fermat_probs, miller_rabin_probs)
    print(f"\nPlot saved as {plot_file}")

if __name__ == "__main__":
    main()