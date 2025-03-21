from collections.abc import Iterable
from io import TextIOWrapper
from typing import Iterator, Union

from toy_gc_content.exceptions import BadFastaInput


def gc_content(fasta: Union[TextIOWrapper, Iterator[str], str]) -> float:
    """
    Calculate the GC content from FASTA input containing DNA sequences.
    The input can be:
    * An open file object (TextIOWrapper)
    * An iterator yielding strings
    * A FASTA format string (e.g. ">test_sequence\nGCCAAAT\nTTT\n")

    Args:
        fasta: A FASTA format input containing DNA sequences. Each sequence should have
             a header line starting with '>' followed by one or more lines of sequence.
        
    Returns:
        float: The GC content as a fraction (0.0 to 1.0)
        
    Raises:
        BadFastaInput: If the input is bad, e.g., no DNA sequences are found in the input
    """
    total_bases = 0
    gc_count = 0
    
    # A str is an Iterable of chars, so the order in which we do the type-checking here matters.
    if isinstance(fasta, str):
        return _gc_content(fasta.splitlines())
    elif isinstance(fasta, Iterable):
        return _gc_content(fasta)
    else:
        raise BadFastaInput(f"Unsupported FASTA input type: {type(fasta)}")

def _gc_content(fasta: Iterator[str]) -> float:
    """
    Calculate the GC content from FASTA input containing DNA sequences.
    This helper method operates on a string iterator. The front-end function is
    responsible for converting the input into an iterator.
    
    Args:
        fasta: FASTA format input containing DNA sequences, provided in a string iterator.
        Each sequence should have a header line starting with '>' followed by one or more
        lines of sequence.
        
    Returns:
        float: The GC content as a fraction (0.0 to 1.0)

    Raises:
        BadFastaInput: If the input is bad, e.g., no DNA sequences are found in the input
    """
    total_bases = 0
    gc_count = 0
    
    for line in fasta:
        #print(f"Processing line: {line.strip()}")
    
        # Skip header lines and empty lines
        if line.startswith('>') or not line.strip():
            continue
    
        if not isinstance(line, str):
            raise BadFastaInput("Fasta iterator must yield only strings")
    
        sequence = line.strip().upper()
        total_bases += len(sequence)
        gc_count += sequence.count('G') + sequence.count('C')
    
    if total_bases == 0:
        raise BadFastaInput("No sequences found in the fasta input")
        
    #print(f"GC count: {gc_count}, Total bases: {total_bases}")
    return gc_count / total_bases