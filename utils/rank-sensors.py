#!/usr/bin/env python3
import pandas as pd
import sys

df = pd.read_csv(sys.stdin, dtype={'valid': bool})

r = df.groupby(['subsystem', 'sensor', 'parameter'])['valid'].agg(['sum', 'count'])

r['total'] = r['count']
r['valid'] = r['sum']
r['invalid'] = r['count'] - r['sum']
r['ratio'] = r['sum'] / r['count']

with pd.option_context('display.multi_sparse', False):
    print(r[['total', 'valid', 'invalid', 'ratio']].sort_values(['ratio', 'subsystem', 'sensor', 'parameter']).reset_index().to_string(index=False))
