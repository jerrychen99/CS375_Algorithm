import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file, sort_pairs, generate_random_input_file

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
    strip.sort(key=lambda point: point[1])
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

def divide_and_conquer_closest_pair(points):
    def find_closest_pairs(points):

        points = sorted(points, key=lambda point: point[0])
        
        n = len(points)
        if n <= 3:
            return brute_force_closest_pair(points)

        mid = n // 2
        midpoint_x = points[mid][0]
        left_points = points[:mid]
        right_points = points[mid:]

        dl, left_closest_pairs = find_closest_pairs(left_points)
        dr, right_closest_pairs = find_closest_pairs(right_points)

        d = min(dl, dr)
        closest_pairs = left_closest_pairs + right_closest_pairs if dl == dr else (left_closest_pairs if dl < dr else right_closest_pairs)

        strip = [point for point in points if abs(point[0] - midpoint_x) < d]
        strip_distance, strip_pairs = closest_pair_in_strip(strip, d)

        if strip_distance <= d:
            combined_pairs = closest_pairs + strip_pairs if strip_distance == d else strip_pairs
            combined_pairs = [(tuple(pair[0]), tuple(pair[1])) for pair in combined_pairs]
            return strip_distance, sort_pairs(list(set(combined_pairs)))
        else:
            return d, closest_pairs

    points = [tuple(point) for point in points]
    closest_distance, closest_pairs = find_closest_pairs(points)

    return round(closest_distance, 4), closest_pairs


if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        min_dist, closest_pairs = divide_and_conquer_closest_pair(points)
        
        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'output_divideandconquer.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)