#!/usr/bin/env python3
import pandas as pd
import sys

df = pd.read_csv(sys.stdin, dtype={'valid': bool})

r = df.groupby('node_id')['valid'].agg(['sum', 'count'])

r['total'] = r['count']
r['valid'] = r['sum']
r['invalid'] = r['count'] - r['sum']
r['valid_ratio'] = r['sum'] / r['count']
print(r[['total', 'valid', 'invalid', 'valid_ratio']].sort_values(['valid_ratio', 'node_id']).reset_index().to_string(index=False))
