# [FacebookHackerCup-2020](https://www.facebook.com/hackercup/past_rounds/) ![Language](https://img.shields.io/badge/language-Python-orange.svg) [![License](https://img.shields.io/badge/license-CC%203.0-blue.svg)](https://creativecommons.org/licenses/by-nc/3.0/) ![Progress](https://img.shields.io/badge/progress-17%20%2F%2018-ff69b4.svg)

Python solutions of Facebook Hacker Cup 2020. Solution begins with `*` means it will get TLE in the largest data set (total computation amount > `10^8`, which is not friendly for Python to solve in 5 ~ 15 seconds). A `6-minute` timer is set for uploading the result this year.

* [Hacker Cup 2019](https://github.com/kamyu104/FacebookHackerCup-2019)
* [Qualification Round](https://github.com/kamyu104/FacebookHackerCup-2020#qualification-round)
* [Round 1](https://github.com/kamyu104/FacebookHackerCup-2020#round-1)
* [Round 2](https://github.com/kamyu104/FacebookHackerCup-2020#round-2)
* [Round 3](https://github.com/kamyu104/FacebookHackerCup-2020#round-3)

## Qualification Round
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Travel Restrictions](https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/A)| [Python](./Qualification%20Round/travel_restrictions.py)| _O(N^2)_ | _O(1)_ | Easy | | Two Pointers |
|B| [Alchemy](https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/B)| [Python](./Qualification%20Round/alchemy.py)| _O(N)_ | _O(1)_ | Easy | | Math |
|C| [Timber](https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/C) | [Python](./Qualification%20Round/timber.py) | _O(NlogN)_ | _O(N)_ | Medium | | DP |
|D1| [Running on Fumes - Chapter 1](https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/D1)| [Python](./Qualification%20Round/running_on_fumes_chapter_1.py) | _O(N)_ | _O(M)_ | Medium | | Mono Deque |
|D2| [Running on Fumes - Chapter 2](https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/D2)| [Python](./Qualification%20Round/running_on_fumes_chapter_2.py) | _O(NlogN)_ | _O(N)_ | Hard | | DFS, BFS, Segment Tree |

## Round 1
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A1| [Perimetric - Chapter 1](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/A1)| [Python](./Round%201/perimetric_ch1.py)| _O(N)_ | _O(N)_ | Easy | | Mono Deque |
|A2| [Perimetric - Chapter 2](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/A2)| [Python](./Round%201/perimetric_ch2.py)| _O(NlogN)_ | _O(N)_ | Medium | | Skip List, Line Sweep |
|A3| [Perimetric - Chapter 3](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/A3) | [PyPy](./Round%201/perimetric_ch3.py) | _O(NlogN)_ | _O(N)_ | Hard | | Skip List, Line Sweep |
|B| [Dislodging Logs](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/B)| [Python](./Round%201/dislodging_logs.py) | _O(NlogN + MlogM + (M + N) * log(max(max(Q)-min(P), max(P)-min(Q))))_ | _O(N + M)_ | Easy | | Binary Search, Greedy |
|C| [Quarantine](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/C)| [Python](./Round%201/quarantine.py) | _O(N)_ | _O(N)_ | Hard | | Preorder Traversal, Flood Fill, DP |

## Round 2
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Ca-pasta-ty](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-2/problems/A)| [Python](./Round%202/capastaty.py)| _O(N)_ | _O(1)_ | Easy | | Math |
|B| [Elimination](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-2/problems/B)| [Python](./Round%202/elimination.py) | _O(N^2)_ | _O(N^2)_ | Medium | | Math, DP |
|C| [Circular Circles](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-2/problems/C)| [PyPy](./Round%202/circular_circles.py) | _O((N * M + E) * (logN + logM))_ | _O(N)_ | Medium | | Skip List |
|D| [Log Drivin' Hirin'](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-2/problems/D)| [Python](./Round%202/log_drivin_hirin.py) | _O(N * (logN)^2 + MlogN)_ | _O(N)_ | Hard | | Skip List, Dynamic Convex Hull Trick |

## Round 3
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|A| [Chain Explosions](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-3/problems/A)| [Python](./Round%203/chain_explosions.py)| _O(K^(1/2))_ | _O(1)_ | Easy | | Math |
|B| [Railroad Renovations](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-3/problems/B)| [Python](./Round%203/railroad_renovations.py) | _O(N^3)_ | _O(N * K)_ | Medium | | DP, Math |
|C| [Mail Security](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-3/problems/C)| [PyPy](./Round%203/mail_security.py) | _O((N + M) * (logN + logM)^2)_ | _O(N + M)_ | Hard | | Binary Search, Skip List, Greedy |
|D| [Smart Carts](https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-3/problems/D)| | _O(N^3)_ | _O(N)_ | Hard | | |
