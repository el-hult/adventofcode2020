This year has an AoC as well. https://adventofcode.com/2020

I'll work in python 3.12 this time.
formatting and linting with `uvx ruff format`

# Running
Download the inputs using curl if you first get a session cookie e.g. from the browser.

```bash
for i in $(seq 1 24); do j=$(printf "%02d" $i); curl --cookie "session=somelongvalueforthesessioncookie" "https://adventofcode.com/2020/day/$i/input" -o day$j.txt; done
```

Then run code using e.g. `uv run day01.py`. It should be silent if it is correct to my output.

If you want timing for each run, in bash you can run
```bash
for f in day*.py; do t=$( { time uv run "$f" >/dev/null; } 2>&1 | grep real | awk '{print $2}'); echo -e "$f\t$t"; done
```

# Before commit

Make sure all code runs, there is no output, and all tests pass.

```bash
uvx ruff format
for f in $(ls day*.py); do uv run $f; done
uvx python -m unittest
```

# Reflections on each day

# Day 23

In day 23, we need to rearrange a bunch of objects many times, organized in a circular buffer. Task two is just a larger version of task 1.

If we use an array to manage the circular buffer there will be a lot of copying to do, so I instead use a linked list where each node in the list can hold a value and a pointer to the next node. I use `dataclass` for this, since `namedtuple` is not mutable.
Creating the linked list was more expensive than actually running my algorithm, so using a single array holding the next-pointers, (that `ptrs[k-1]` would hold the cup to the right of cup number `k`) would give a significant speedup. But the code would be uglier, and I would make mistakes, so it was not my first choice of implementation.
The dataclass solution was fast enough for now anyways (ca 4 seconds for part 1 and 2 combined).

# Day 22

Part one was just a simple implementation of the game of combat. It was almost trivial.

Part two also went super smooth. Some tiny optimizations I did from the very start was:

- use a `deque[int]` for the player decks to get O(1) pop from the left. In the normal game of Combat, this was a tiny optimization, but seems nice, still. In a recusrive game, this was actually a non-optimization! In each recursive game we must slice the hands, and a `deque` cannot be sliced, forcing a conversion to list, which is expensive. Going back to `list[int]` saved me a bunch of time.
- use a `set` for the of seen states, to stop infitnite recursive games, for quick lookups.
- only store the hashes of the seen states, in a `set[int]`, which saves memory, a lot of allocations, and thus increases speed quite a bit.

One could worry about recursion depth -- can we implement the game with function call recursion, ot must we explicitly have a stack of ongoing games and use some for loop? The largest card value is smaller than 99, so the maximum recursion depth is smaller than 100, which the python call stack should handle well.

To hash the states I must convert the hands to some hashable type (tuple, not list/deque) and I suspect this is a little costly. 
In a compiled language I would use some nice data type specific hasher, since I really just need to hash two int streams.
It is concievable a custom hasher in python could speed up things too. 

# Day 21
This day is about logical inference. We need to deduce allocation from allergens to ingredients.
Each allergen is found in exactly one ingredient.
Each ingredient contains zero or one allergen.
An food item may have undeclared allergens.
I will assume that all allergens are present at least once in the input -- otherwise the problem is not well defined.
So the three foods could be listed as

A B C     (contains peanuts, fish)
A   C D
A B   D   (contains peanuts, lactose, soy)
A       E


My first attempt was to just see if the input permitted a more naive solution, analyzing one allergen at a time.
From the above example, we could take each allergen and see what ingredients it could potentially come from. Considering 'peanuts', the first line says it is in either A, B or C. Food 2 does not contradict that.
Food 3 tells us peanuts is in either A, B or D. We take the intersection of these lists to find peanuts must be in A or B. We can also conclude that C and D cannot contain peanuts, since they show up in a list where peanuts is declared, but not in every list where peanuts is declared.
From food 3 we find that A, B and D all contain some allergen, but not fish. So fish must be in C, considering food 1 again.
We can also -- from food 1 and 2 -- deduce that A, B, C and D all contain allergens, and thre are in total 4 allergens. So E must be free from allergens.
Part one of the day 21 is to find all ingredients that do not contain allergens, and count their number of occurences..

Solving the full problem of allocations reminds me of sudoku... Allocating numbers to cells, and the boxes/rows/columns make it possible to exclude certain allocations.
The systematic way to solve this kind of problem is to cast it as a SAT problem. But SAT solving is esseentially exhaustive search with good heuristic identification that can cut down the search space. I suppose a specialized solver will be better in this problem instance, instead of casting it as a generic SAT problem...

For part one, it was enough to consider each allergen independently; check per allergen what the intersection of the possible ingredients are, to create a candidate set of ingredients per allergen.
The ingredients that don't show up there must not contain allergens, so we can count them. This was enough for my specific input.

With this candidate list, we can brute force test all solutions; there is 8 allergens with only a few possible ingredients each.
But looking at the data again, we can see a greedy allocation will be enough!
One allergen had a single candidate ingredient.
Then we can exclude that ingredient from the allocation lists of the other allergens.
Repeating that that process, one allocation at a time, solves the problem.

# Day 20
Part one is about filling a square grid with tiles, like a jigsaw puzzle. Each tile can be rotated and flipped. I do this brute force.
Some minor optimizations were implemented. To keep the branching factor small, I did DFS with filling in row major order. A lot of expensive python copy operations. :(

In part 2 I need to do some simple pattern recognition. I assumed no sea monsters overlap, and that worked.
I also assum there is only one orientation of the image where there are any sea monsters, so I can try all 8 orientations and just work with the first one with any sea monster.

Overall, this day was not really hard for me, but it took a lot of code, and I had a bunch of bugs related to my implementation rather than the algorithm I chose.

# Day 19

Part one is about parsing expressions and see if they conform to some grammar.
It is given there is no recursion in the grammar, so it is regular, and regexes can solve the problem. 
It worked great for part one. Probably not very efficient, but still fast enough. I quite a bit of time trying to implement a regex engine myself for this, inspired by https://www.0de5.net/stimuli/fun-and-games-generating-dfas-from-regular-expressions, but eventually I gave up. Too slow. Too complicated. I ended up using the `re` module in python instead. 

For part two, we get two new production rules. The first one is 
```
8: 42 | 42 8
```
which we recognize as "one or more 42s", a common thing for regexes to find using the `+` operator.

The second new rule is
```
11: 42 31 | 42 11 31
```
and this is not a acceptable form in a regular grammar. In a regular grammar, the nonterminal symbols must be on the left or on the right hand side in the production rules, and while 42 and 31 can be replaced by terminal symbols (due to the tree-structure in the grammar), the precence of the 11 in the middle ruins everything.

To solve this, I realized that the rule `0: 8 11` makes things easier. It is enough to see if the message has `m` `42`s and `n` `31`s, where `m >= n + 1`. 
I tried doing this greedily, and that worked. If we were unlucky, we might have to try to parse some `m' < m` `42`s in case `42` and `31` have overlapping patterns. 
But I did not have to do that.
To parse the `31` and `42` patterns, I just used the same regexes as before.


# Day 18

This day was about parsing arithmetic expressions, considering operator precedence and parantheses. 
Part one, I could implement myself with a simple state machine, because one only needed left associativity and parentheses.

For part two, I read up a little on PRATT parsers, operator climbing, and finally found the shunting yard algorithm. The last one was the simplest, but still solved my problem. Because there are no unary operators, a small simplification was possible. I created the intermediate Reverse Polish Notation expression for debugging as well, even though it was not really needed. I suppose I could have saved a tiny bit of memory there. The algorithm is not terribly interesting, and I cannot say I really learned it. 

With the part_two solver, I could solve part_one with same code by just changing operator precedence, simplifying my code a little.

# Day 17
Day 17 is about running cellular automata in 3D and 4D. At first, I got the wrong answer, and was very confused. After rewriting a bit, making the code simpler (at the cost of a little performance) I got the right answer. Instead of 
```
if cell.active and cell.neighbors == 2 or cell.neighbors == 3:
  cell.stay_active()
elif cell.inactive and cell.neighbors == 3:
  cell.become_active()
```

I had implemented

```
if cell.active and cell.neighbors == 2 or cell.neighbors == 3:
  cell.set_active()
elif cell.inactive and cell.neighbors == 3:
  cell.set_inactive()
```
which was a combination of misunderstanding the rules + implementation bug.
I was confident in my misunderstanding and my code was so noisy I did not realize it.
I found out my mistake by writing a more naive implementation, with less code and noise.

**Insight:** Initially, I had a `defaultdict` with boolean values to represent the board, where `state((x,y,z))` what whether the cell at `(x,y,z)` was active or not. Reading online trying to understand the problem I realized that using a simple `set` makes more sense, since I don't really need to store all the `false` entries. This neater API simplified the code a bit, and helped in finding the bug above.

**Insight:** The whole space is mirror symmetric around the z=0-plane, so only half the space needs to be simulated for part one.  In part two, we have mirror symmetry in $w=0$ as well, so here, we should be able to cut runtime by 4 using this trick. I have not made this optimization, since it would make the code uglier.

**Insight:** I recompute the bounds of the simulation in each round, which is possibly ugly, since I iterate the active cells many times. Using a data structure to cache that might speed up the simulation. I did that before, but it is part of why the code got noisy and buggy, so I refrained from doing that now.

# Day 16

I found this quite fun. The part 1 was simple, because the most naive solution was fast enough. Just step through the tickets and rules and check everything. No need to be clever.

Part 2 I solved in steps. I realized we are to find an allocation of field names to columns, and we have rules based on observed tickets that makes certain allocations impossible. This is a permutation, and permutations can be shown as a matrix with 0/1 entries. I computed the matrix where a 0 means this row (field name) cannot be allocated to this column (field number). A 1 meant 'maybe', and I must try what allocations are compatible with this. I created a DFS search to just brute my way through the possible allocations. To be more concrete: in the matrix below, how can you flip 1s to 0s, so that in the end every row and every column as exactly one 1?
```
[[0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
 [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
 [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
 [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]
```

Solving this with DFS, starting at the first row, going down, was too slow. I realized that I should start with allocating rows that are constrained more (some rows have very few 1s) so that early allocations are more likely to be correct.
So I sorted my "potential allocations" matrix by the number of 1's in each row and found that this heuristic was great!

```
[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
 [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
 [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
 [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
 [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
 [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
```
Sorting revealed that every row has only one more 1 than the row above it, and all the other 1s are in the same column as above. So greedy allocation will work, and no backtracking needed!
This solution was super fast, and I am happy with this insight from looking at data.


# Day 15
My quite naive solution was fast enough on my hardware. It takes 6 seconds to run at time of writing for part 1 and part 2. The only optimization I did was to have a hashmap of "last spoken when" to avoid keeping this full history in memory a doing slow linear searches in that.

The hashmap feels like it should be slow though, with much overhead. Can we try other data structures instead?

Moving to a list instead made the runtime go to 3.6 seconds instead of 6.1 seconds.
My insight was that the numbers can never be larger than the number of turns I want to check for, so I can allocate all memory in the beginning, and do array lookups instead of hashmap lookups.

I even tried using an array from the `array` module, but this did not improve performance. Those fixed-size arrays are not really faster, just more memory efficient.


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
