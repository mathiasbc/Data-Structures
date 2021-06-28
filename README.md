# Python Data Structures

I put together this repository while preparing for a round of technical interviews
for the Software Engineer Developer position.


## Binary search Tree

height = 2
nodes = 2 ^ (height + 1) - 1 == 7

         6                  h=0
       /   \
      4     8               h=1
     / \   / \
    3   5 7   9             h=2


### Traversal techniques:
    In-order:   3, 4, 5, 6, 7, 8, 9  -> returns ordered elements
    Pre-order:  6, 4, 3, 5, 8, 7, 9  -> good for dumping to array/serialize
    Post-order: 3, 5, 4, 7, 9, 8, 6  -> good for deleting, does not alter not without children


### Search techniques (exploration):
    BFS:        6, 4, 8, 3, 5, 7, 9
    DFS:        6, 4, 3, 5, 8, 7, 9


### List representation:

```
    _____________________________
    | 6 | 4 | 8 | 3 | 5 | 7 | 9 |   -> Node (value)
    -----------------------------
    | 0 | 1 | 2 | 3 | 4 | 5 | 6 |   -> position (i)
    -----------------------------
```

    root: list_tree[0]
    Left child: (2*i)+1
    Right child: (2*i)+2
    Parent: (i-1)/2
