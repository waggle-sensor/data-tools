#!/usr/bin/env python3
import pandas as pd
import sys

df = pd.read_csv(sys.stdin, dtype={'valid': bool})

r = df.groupby('node_id')['valid'].agg(['sum', 'count'])

r['total'] = r['count']
r['valid'] = r['sum']
r['invalid'] = r['count'] - r['sum']
r['ratio'] = r['sum'] / r['count']
print(r[['total', 'valid', 'invalid', 'ratio']].sort_values('ratio').reset_index().to_string(index=False))
