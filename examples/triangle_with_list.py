from typing import List, Set, Dict, Tuple, Optional

def triangle_with_list(a: List[int], b: int, c: int) -> int:
    if a[0] == b:
        if a[1] == c:
            if b == c:
                return "Equilateral"
            else:
                return "Isosceles"
        else:
            return "Isosceles"
    else:
        if b != c:
            if a[4] == c:
                return "Isosceles"
            else:
                return "Scalene"
        else:
            return "Isosceles"