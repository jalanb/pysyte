The versions module
===================

    >>> from pysyte.devops import versions
    >>> assert "versions for pysyte" in versions.__doc__


The Versions class
------------------

    >>> Version = versions.Version

Make versions from strings or lists

    >>> assert Version("2.3.5") == Version((2, 3, 5)) == Version((2, "3", 5))

Attributes

    >>> version = Version("2.6.m")
    >>> assert version.major == "2"
    >>> assert version.minor == "6"
    >>> assert version.patch == "m"
    >>> assert isinstance(version.production, Version)
    >>> assert version.production == "2.6"
    >>> assert version.split() == ("2", "6", "m")

Can compare versions

    >>> Ver = Version
    >>> assert Ver("3.9.9") < Ver("3.9.10") < Ver((7, 3)) < Ver("10.0.0")

Numbers are compared, not strings

    >>> assert Ver([9]) == Ver("9") < Ver("10") == Ver([10])

Letters are always lower than digits

    >>> assert Ver("2.3.z") < Ver("2.3.0")

Case is not sensitive

    >>> assert Ver("8.9.a") == Ver("8.9.A")

Can have more than 3 parts

    >>> assert Ver("3.4.v.merge").patch == "v.merge"


