This year has an AoC as well. https://adventofcode.com/2020

I'll work in python 3.8 this time.

# Day 5
It seems the challenge of today was about understanding binary numbers.
Given that, it was not very hard.

I like the `itertools.starmap` and `map` functions, but I actually think a list comprehension would be more pythonic and readable.
I guess I would revert to that if my code would fail me. 
But as long as it works correctly on the first run, I guess there is no harm in writing it like this...

To search for a missing boarding pass seat ID, I used set difference. That seemes like a fun way to do it. :) 
It is definitely not the fastest way. I _should_ use the fact that we are working with a list of ints, in some way, so there should be a faster way to do it...

# Day 4

Today was a real pain. I used 
```python
pid = re.compile("[0-9]{9}").match(passport['pid'])
```
to find a 9 digit number. I should have used 
```python
pid = re.compile("^[0-9]{9}$").match(passport['pid'])
```
And that took me HOURS to figure out. Otherwise it was fun.

This error made it so that one single passport validated when it shouldn't. That passport had 10 digigts instead of 9, but the regex still matched. This error type was not present in the test data presented in the challenge. I even had to take a sneek peak in the solution of Thomas Aschan to see what went wrong.

One learning is that I made my checked on the parsed data, and my errors was in parsing. So my error was not detectable...

# Day 3
part a was simple and straight forward.

part b was trickier, since I made a logic error in the 2-steps-down code. and it is NOT pretty to debug nested generator and comprehension expression. In fact, I translated the code to for-loops to debug, found a division-error, and fixed it in my generator code, and then it worked.

so i guess the learning is that generator code is nice to write, but not to analyze.

still I kept it because i think it looks neat. :)

# Day 2
This time, I got to use `collections.Counter` which is nice. It is probably very inefficient since it counts the occurances of every character type, but I guess it provides some nice semantics at least.
Also, I used a bit of `re.match` to parse the lines. that seemes reasonable to avoid splitting by character, and the lines did not have a fixed width format....

For part B, there was nothing fancy. I did the proper parsing the first time, so just adding another rule was very staright forward/

# Day 1
A nice little "work with a list" type of thing.
I went for a haskell'y generator based approach.
This way I don't need to think about how long the list is and whether the list of all products fit in memory etc.
It is day1 however so I guess there would be no problem.

To solve part B, I rewrote the code a little so it could handle both cases.
