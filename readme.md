This year has an AoC as well. https://adventofcode.com/2020

I'll work in python 3.8 this time.


## Before commit

Make sure all code runs, and there is no ugly output.

```
flake8
black .
python -m unittest
gci day*.py | %{ new-object PSCustomObject -Property  @{file=$_.Name;runtime_millis=[math]::Round((Measure-Command {python $_}).TotalMilliseconds)}}
```

## Timing
To run all my solutions and see performance, run
```powershell
gci day*.py | %{ new-object PSCustomObject -Property  @{file=$_.Name;runtime_millis=[math]::Round((Measure-Command {python $_}).TotalMilliseconds)}}
```

Running the same program a few times to get an average is also simple:
```
 1..10 | %{Measure-Command {python day11.py} }| measure -Property TotalMilliseconds -Average
 ```

Also - to get some better insight into some specific day and shy it runs slow, run 
```powershell
python -m cProfile day11.py
```

## Testing
At day 14 I needed to run some test code... I do that with `unittest` and standard code convenstions so that `python -m unittest` does the discovery alright.

I have also added the 
```
if __name__ == "__main__":
    unittest.main()
```
code so that `python test_dayXX.py` works for running a single file (very nice if your IDE has a 'run this file' feature').

# Day 14

Part A was a simple thing. I realized bit operations would make this fast and simple, so I read a line or two on wikipedia and implemented a fast solver. Piece of cake.

Part B is a different beast however...

So my first attempt was to write a super complicated code that has memory adresses with X's in them, so that one adress refers to may places in memory. The downside is that the older writes may have overlaps with the new memory write instruction, thus needing complicated logic to resolve these conflicts. At my first attempt it did not get right (also worth mentioning is that the bugs I created and found before submitting the answer were numerous.)

After the first bad submssion, I realized I only corrected single-position collisions. That was fixed quite quickly by adding more test cases. Implementing some not-so-clever logic to repeatedly apply the splitting logic fixed the problem.

This challance was BY FAR harder than the others.

I guess one could brute force part B as well. I didn't even try that. In the end my memory had 1285 records in it. I claim that is quite okay. It is much better than implementing the whole 36 bit memory that should hold 36 bit ints. That would need 36*36=1296 bits in total, so I guess that is acceptable. If I had contigous memory access that would be all okay. But I feel there is a huge risk that the overhead of python will prevent a brute force ``attack''.

Im happy I'm done for now.

...okay I ran the linter with check for complexity. And due to that I've now extracted some stuff into a separate function and such cleanup. Feels much better now. :)


# Day 13 

Part A was silly simple. I don't get what was up with that...

Part B is trickier. To take the example bus schedule from the instruction, we want to solve for the minimal `t` such that

```python
buses = [(0, 7), (1, 13), (4, 59), (6, 31), (7, 19)]
for i,b in buses:
  assert (t+i) % b == 0
```

First make a small recasting to 

```python
for i,b in buses:
  a = -i % b
  assert t % b == a
```

After a lot of contemplation I realized all the `b` are pairwise coprime!
So that means we want to find a solution using the [Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem) that I learned about in school ~8 years ago... 

I implemented the method by sieving described on wikipedia.

**Remark:** When solving this problem I had a huge detour into rewriting the problem as a linear Diophantine system. That is also described a little in Wikipedia, so it is a possible angle to attack the problem. But less efficient. And more complicated to code. The sieving is fast enough!


# Day 12

Part a was cute and fun. I had some ideas about using a pure iterator-reducer style here. I think that will be a pain for part B, but I wanted that still. It went well after some spaghetti coding. 

Part B needed a little reriting. Specifically, since it works with another state variable structure, It needs a separate handler.
I wanter to also use the elementary `translate` and `rotate` in all the code, so I made some rewriting of the previous code to facilitate that. I also spent some time cleaning up the code in the end.

The unifying idea is tha a facing direction can be thought of as having a waypoint in front of the face, and rotation of the waypoint and rotation of the ship is the same thing. Please look at the separate git commits to compare!

In the end, I was quite happy with the amount of code reuse and so on. :)

# Day 11

I made an off-by-one error here. Here is a quite contrived examlpe that shows the problem:

```python
imax = max(d.keys()) # save what the largest key is
d[imax+1] = 1 # now we cannot loop over the keys, but need to use the keys from before..
for i in range(imax): # iterate over the original keys
  do_stuff(d[i])
```
In this case, since `range()` never reaches the end index you skip the last entry in the array. But otherwise part A was nice and easy.

Part B proved no logical problem. A misread about whether to look at the next *seat* or the next *occupied seat* in each direction. But it was fine after fixing that logical mistake. My solution is very slow though... I guess that is because of the generator overhead everywhere. But that is fine still. A few seconds...

**Remark** Okay I did go back and run a profiler. It is indeed the generator overhead that is the bad thing here. 😞 So I would need some simpler logic (more imperative?!) to make this go faster. I had to remove my whole `ray` logic, that I thought was clever. By using the same logic - but not with a lot of generator expressions - cut the runtime in half or so. To go further, I probably need to do more clever things such as precomputing what the "neighboring seats" are for each seat according to the 'real' topology of the map, or according to the 'line-of-sight-tolopoly'. This way there will be a few hash map lookups to count the neighbors, instead of... a lot.


# Day 10

In part (a), we can use the fact we must traverse the voltages in the order that is always taking the smallest step. So sorting them, taking the steps and counting what steps you take is enough. Very succint oneliner.

In part (b) stuff was more difficult. To brute force it head on is not possible. I utilize that between all adapters there is a 1 or 3 volt difference. 
If there is a 3 volt diff, I *have* to select both adapters. If there is a contigous chunk or 1 voltage drops, I can choose what adapters to include or not in this chunk, but not caring about how I chose in *other* contigous chunks. So the number of possible choices overall is the product of choices per chunk.

The last part could be written in a super condensed oneliner, I think. Itertools for the win... But that would not be readable AT ALL. So I chose an imperative style, but with some iterator for loops at least.

# Day 9
Im curious why this is so easy. Just throwing itertools at the problem seems to do the trick. It is fast enough so there is no need to be clever here....

The one curious bit is the `window` function that used to be part of the `itertools` recipies, but was deleted for the advancement of `pairwise`.
I found a recipie online that I used instead. It was good enough (the direct generaliztion of `pairwise`)


# Day 8

This was boring. Lind of like the good ol' bitcode computer from last year. Straight forward implementation.

# Day 7

Today was quite okay. But I still think it is a pain to write graph traversal algorithms. I understood already from partA that it made sense to parse the graph so it could be traversed in both directions.
For part A it was a simple DFS search to count the number of leafs going in the "the bag is being held by"-direction.

For part B, the multiply-and-sum effectively eliminates any nice tail call style recursion, and the recursion depth was exceeded quickly. Therefore, some state management was needed. It was not very complicated however. To save some work, I kept an index of all already computed bags.

There was only one point where I stumbeled. It went like the following.
I planned to do DFS: For each node you visit see if you can compute its value (possible if all children has been processed before). if you can. good! if you cannot, first put the node on the stack for later revisit, and then put all children on the stack of nodes to visit. skip the nodes that are already computed, and the ones that are already in the stack to be visited. next, pop a new node from the stack and visit it.
```
A
|\
B |
| |
D |
 \|
  C
```
Running this strategy on the above graph, one could have a problem. First we visit A and add B and C to the list of nodes to visit. Then we visit B and add D. Then we visit D. But we don't want to add C, since it is already in our list of nodes to visit. 
But since C is not computed, we cannot compute D. So this is a loop. One solution is to add C anyways, and skip it the next time we pop it from the stack.
I chose the solution to simply put D in the bottom on the stack, and inspect the next, popping B. Then pop C. Compute it. Pop A. realize it is not computable and add it to the bottom of the stack. But now we can pop D! Comput it. Then compute B. Then compute A. That works. It is not the most efficient, but it was easy to write, and was good enough.

# Day 6
This day was really easy, I think. It lent itself to iterator style programming.
A lot of map-reduce kind of logic.
When it nested in part B, I chose to change to an imperative style.

I really like the `collections.Counter` method. It sure helps writing semantically clear code, and I think that it is helpful. It is maybe not the fastest, but what the heck. It is good enough!

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
