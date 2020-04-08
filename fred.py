from pysyte.config import urator
from pysyte.types.paths import tmp
path_to_config = tmp() / 'test.yamly'
path_to_config.write_lines(['---', 'fred: 1',])
path_to_config = tmp() / 'test.yamly'

