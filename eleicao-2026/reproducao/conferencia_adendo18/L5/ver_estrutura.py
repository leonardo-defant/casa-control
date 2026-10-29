import gzip, json, sys
d = json.load(gzip.open(sys.argv[1], 'rt'))
print(type(d), len(d))
k = next(iter(d)); print(k, d[k])
c = json.load(gzip.open(sys.argv[2], 'rt'))
print(c.keys() if isinstance(c, dict) else type(c))
s = c['secoes']; k2 = next(iter(s)); print(len(s), k2, s[k2])
