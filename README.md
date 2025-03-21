Toy package to analyze GC content in FASTA files.
See https://en.wikipedia.org/wiki/GC-content for more info.
I'm just having fun here, this library is not intended for real use.

There are two functions you can call:

* gc_content - scans DNA sequence data in FASTA format and returns the percentage of GC content, as a number between 0 and 1. The input can be:
  * An open file object (TextIOWrapper)
  * An iterator yielding strings
  * A FASTA format string
* gc_content_s3 - does the same analysis on a FASTA object stored in AWS S3. The input is the S3 URL for that object.
