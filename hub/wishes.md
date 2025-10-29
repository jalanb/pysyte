# Wishes

## DDD

aka Doctest Driven Development

## Doctest a public interface for this library

Find everything else that imports it:
 - "$ ack from.pysyte ~/jalanb/pysyse/__main__"
 - "$ ack from.pysyte ~/jalanb" (excluding `~/jalanb/pysyse`)

Then, for every example usage of the library in other projects
  - there should be an exemplary doctest in the library
  - in the most appropriate block of code

Once you have the minimal public interface
- then YAGNI for whatever more code is in the library
 - There is a __lot__ of YAGNI in `pysyte`
 - needs pruning
