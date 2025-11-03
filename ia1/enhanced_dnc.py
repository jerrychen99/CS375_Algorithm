import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file, sort_pairs

def brute_force_closest_pair(points):
    min_dist = float('inf')
    closest_pairs = []

    for point1, point2 in combinations(points, 2):
        dist = distance(point1, point2)
        if dist < min_dist:
            min_dist = dist
            closest_pairs = [(tuple(point1), tuple(point2))]
        elif dist == min_dist:
            closest_pairs.append((tuple(point1), tuple(point2)))

    return round(min_dist, 4), sort_pairs(closest_pairs)

def closest_pair_in_strip(strip, d):
    min_distance = d
    closest_pairs = []

    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if strip[j][1] - strip[i][1] > min_distance:
                break
            dist = distance(strip[i], strip[j])
            if dist < min_distance:
                min_distance = dist
                closest_pairs = [(tuple(strip[i]), tuple(strip[j]))]  
            elif dist == min_distance:
                closest_pairs.append((tuple(strip[i]), tuple(strip[j])))  

    return min_distance, sort_pairs(closest_pairs)

def enhanced_divide_and_conquer_closest_pair(points):
    def find_closest_pairs(px, py):
        n = len(px)
        if n <= 3:
            return brute_force_closest_pair(px)

        mid = n // 2
        midpoint_x = px[mid][0]

        left_px = px[:mid]
        right_px = px[mid:]

        left_py, right_py = [], []
        for point in py:
            if point[0] <= midpoint_x:
                left_py.append(point)
            else:
                right_py.append(point)

        dl, left_closest_pairs = find_closest_pairs(left_px, left_py)
        dr, right_closest_pairs = find_closest_pairs(right_px, right_py)

        d = min(dl, dr)
        closest_pairs = (
            left_closest_pairs + right_closest_pairs
            if dl == dr else (left_closest_pairs if dl < dr else right_closest_pairs)
        )

        strip = [point for point in py if abs(point[0] - midpoint_x) < d]
        strip_distance, strip_pairs = closest_pair_in_strip(strip, d)

        if strip_distance < d:
            return strip_distance, strip_pairs
        elif strip_distance == d:
            combined_pairs = closest_pairs + strip_pairs
            combined_pairs = [(tuple(pair[0]), tuple(pair[1])) for pair in combined_pairs]  
            return d, sort_pairs(list(set(combined_pairs)))  
        else:
            return d, closest_pairs

    points = [tuple(point) for point in points]
    px = sorted(points, key=lambda point: point[0])
    py = sorted(points, key=lambda point: point[1])
    closest_distance, closest_pairs = find_closest_pairs(px, py)
    return round(closest_distance, 4), closest_pairs

if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        min_dist, closest_pairs = enhanced_divide_and_conquer_closest_pair(points)

        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'output_enhanceddnc.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
