# smartTimer

## Config

### Pin Setup
| Timer Name  | Input Pin | Output Pin |
|-------------|-----------|------------|
|    1        |   11      |    16      |
|    2        |   13      |    18      |
|    3        |   15      |    22      |
|   .         |  .        |     .      |

Duplicates are NOT acceptable.

Example:
```CSV
1,11,16
2,13,18
3,15,22
4,29,24
5,31,26
6,33,32
```

### Time Setup
| Timer | Start Time|  End Time |
|-------|-----------|-----------|
|   1   |  1800     |    1900   |
|   2   |  1830     |    1900   |
|   3   |  0500     |    0700   |
|   3   |  0630     |    0900   |
|   4   |  0630     |    0800   |

Duplicates are acceptable.
Time values must be in the following ranges:
0000 - 1159
1200 - 2399

Example:
```CSV
1,1800,1900
2,1830,1900
3,0500,0700
4,0200,0300
5,0300,0500
6,0300,0500
```
