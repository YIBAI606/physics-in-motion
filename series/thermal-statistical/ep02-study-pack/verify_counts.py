from math import comb
from fractions import Fraction
from pathlib import Path
import csv
NA, NB, q = 6, 3, 9
weights=[comb(k+NA-1,k)*comb(q-k+NB-1,q-k) for k in range(q+1)]
total=sum(weights)
assert total == comb(q+NA+NB-1,q)
mean=sum(Fraction(k*w,total) for k,w in enumerate(weights))
modes=[k for k,w in enumerate(weights) if w == max(weights)]
with (Path(__file__).parent/'counts.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.writer(f)
    writer.writerow(['q_A','q_B','multiplicity','probability'])
    writer.writerows((k,q-k,w,w/total) for k,w in enumerate(weights))
print('Total:', total, 'Mean q_A:',mean,'Mode q_A:',modes)
assert mean == 6 and modes == [7]
