from os import read
from util import read_input
from itertools import islice
from math import prod


lns = read_input(3).splitlines()
width = len(lns[0])
print(sum(ln[(3*i)%width]=='#' for i,ln in enumerate(lns)))

print(
    prod(
        sum(
            ln[(right*i//down)%width]=='#' 
            for i,ln
            in islice(
                enumerate(lns),None,None,down)
        )
        for right,down 
        in [(1,1),(3,1),(5,1),(7,1),(1,2)]
    )
    )