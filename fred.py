from pysyte.types import paths

data = ["/Users/jab", "/Users/jab/.bashrc"]
print(paths.directories(data))
print(paths.directories("/Users/jab", "/Users/jab/.bashrc"))
print(paths.directories("/Users/jab"))
print(paths.files(data))
print(paths.paths(data))
