import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file, sort_pairs, generate_random_input_file

def brute_force_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    min_dist = float('inf')
    closest_pairs = []
        
    for point1, point2 in combinations(points, 2):  
        dist = distance(point1, point2)
        if dist < min_dist:                        
            min_dist = dist                        
            closest_pairs = [(point1, point2)]
        elif dist == min_dist:                     
            closest_pairs.append([point1, point2]) 

    closest_pairs = sort_pairs(closest_pairs)

    return round(min_dist, 4), closest_pairs

if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        min_dist, closest_pairs = brute_force_closest_pair(points)

        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'output_bruteforce.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)