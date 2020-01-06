"""Five most popular similarity measures

You won't believe #5, said https://dataaspirant.com/2015/04/11/five-most-popular-similarity-measures-implementation-in-python/

Similarity:

The similarity measure is the measure of how much alike two data objects are. Similarity measure in a data mining context is a distance with dimensions representing features of the objects. If this distance is small, it will be the high degree of similarity where large distance will be the low degree of similarity.

The similarity is subjective and is highly dependent on the domain and application. For example, two fruits are similar because of color or size or taste. Care should be taken when calculating distance across dimensions/features that are unrelated. The relative values of each element must be normalized, or one feature could end up dominating the distance calculation. Similarity are measured in the range 0 to 1 [0,1].

"""

from math import sqrt
from decimal import Decimal

def similar(x, y):
    """Two main consideration about similarity:

    Similarity = 1 if X = Y         (Where X, Y are two objects)
    Similarity = 0 if X ≠ Y
    """
    try:
        setattr(x, 'similar', lambda z: similar (x, z))
        setattr(y, 'similar', lambda z: similar (y, z))
    except AttributeError:
        pass
    return x == y


def euclidean(x, y):
    """Euclidean distance is the most common use of distance.

    In most cases when people said about distance, they will refer to Euclidean distance. Euclidean distance is also known as simply distance. When data is dense or continuous, this is the best proximity measure.

    The Euclidean distance between two points is the length of the path connecting them.The Pythagorean theorem gives this distance between two points.
    """
    return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))


def manhattan(x, y):
    """Manhattan distance is a metric in which the distance between two points is the sum of the absolute differences of their Cartesian coordinates

     In a simple way of saying it is the total suzm of the difference between the x-coordinates  and y-coordinates.

     Suppose we have two points A and B if we want to find the Manhattan distance between them, just we have, to sum up, the absolute x-axis and y – axis variation means we have to find how these two points A and B are varying in X-axis and Y- axis. In a more mathematical way of saying Manhattan distance between two points measured along axes at right angles.

     In a plane with p1 at (x1, y1) and p2 at (x2, y2).

     Manhattan distance = |x1 – x2| + |y1 – y2|

     This Manhattan distance metric is also known as Manhattan length, rectilinear distance, L1 distance or L1 norm, city block distance, Minkowski’s L1 distance, taxi-cab metric, or city block distance.
     """
    return sum(abs(a-b) for a,b in zip(x,y))


def minkowski(x, y, p_value):
    """Minkowski distance is a generalized metric form of Euclidean distance and Manhattan distance
    In the equation, d^MKD is the Minkowski distance between the data record i and j, k the index of a variable, n the total number of variables y and λ the order of the Minkowski metric. Although it is defined for any λ > 0, it is rarely used for values other than 1, 2 and ∞.

    The way distances are measured by the Minkowski metric of different orders between two objects with three variables ( In the image it displayed in a coordinate system with x, y ,z-axes).

    Synonyms of Minkowski:
    Different names for the Minkowski distance or Minkowski metric arise from the order:

    λ = 1 is the Manhattan distance. Synonyms are L1-Norm, Taxicab or City-Block distance. For two vectors of ranked ordinal variables, the Manhattan distance is sometimes called Foot-ruler distance.
    λ = 2 is the Euclidean distance. Synonyms are L2-Norm or Ruler distance. For two vectors of ranked ordinal variables, the Euclidean distance is sometimes called Spear-man distance.
    λ = ∞ is the Chebyshev distance. Synonyms are Lmax-Norm or Chessboard distance.
    """
    def nth_root(value, n_root):
        root_value = 1/float(n_root)
        return float(round (Decimal(value) ** Decimal(root_value),3))

    return nth_root(sum(pow(abs(a-b),p_value) for a,b in zip(x, y)),p_value)
