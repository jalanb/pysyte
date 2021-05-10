"""Some popular similarity measures in python

https://dataaspirant.com/2015/04/11/five-most-popular-similarity-measures-implementation-in-python/

Similarity:

The similarity measure is the measure of how much alike two data objects are.
    Similarity measure in a data mining context is a distance with dimensions
    representing features of the objects. If this distance is small, it will be
    the high degree of similarity where large distance will be the low degree
    of similarity.

The similarity is subjective and is highly dependent on domain and application.
    For example, two fruits are similar because of color or size or taste.
    Care should be taken when calculating distance across dimensions/features
    that are unrelated. The relative values of each element must be normalized,
    or one feature could end up dominating the distance calculation. Similarity
    are measured in the range 0 to 1 [0,1].

"""

from math import sqrt
from decimal import Decimal


def euclidean(x: list, y: list) -> float:
    """Euclidean distance is the most common use of distance.

    Euclidean distance is also known as simply distance.
    When data is dense or continuous, this is the best proximity measure.

    The Euclidean distance between two points is the length connecting them.
    The Pythagorean theorem gives this distance between two points.
    """
    return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))


def manhattan(x: list, y: list) -> float:
    """Manhattan is the the sum of the absolute diff of their Cartesian co-ords

    In a plane with p1 at (x1, y1) and p2 at (x2, y2).
        Manhattan distance = |x1 – x2| + |y1 – y2|

    This Manhattan distance metric is also known as
        Manhattan length,
        rectilinear distance,
        L1 distance or L1 norm,
        city block distance,
        Minkowski's L1 distance,
        taxi-cab metric
    """
    return sum(abs(a - b) for a, b in zip(x, y))


def minkowski(x: list, y: list, p_value: float) -> float:
    """Minkowski distance is general form of Euclidean and Manhattan distances

    In the equation,
        d^MKD is the Minkowski distance between the data record i and j,
        k the index of a variable, n the total number of variables y and
        λ the order of the Minkowski metric.

    Although it is defined for any λ > 0, it is rarely used except 1, 2 and ∞.

    The way distances are measured by the Minkowski metric of different orders
        between two objects with three variables ( In the image it displayed
        in a coordinate system with x, y ,z-axes).

    Synonyms of Minkowski:

    λ = 1 is the Manhattan distance.
    λ = 2 is the Euclidean distance.
        Synonyms are L2-Norm or Ruler distance.
        For two vectors of ranked ordinal variables
            the Euclidean distance is sometimes called Spear-man distance.
    λ = ∞ is the Chebyshev distance.
        Synonyms are Lmax-Norm or Chessboard distance.
    """

    def nth_root(value: float, n_root: float) -> float:
        root_value = 1 / float(n_root)
        return float(round(Decimal(value) ** Decimal(root_value), 3))

    return nth_root(sum(pow(abs(a - b), p_value) for a, b in zip(x, y)), p_value)
