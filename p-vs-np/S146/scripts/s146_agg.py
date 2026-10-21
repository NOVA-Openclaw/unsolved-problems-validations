#!/usr/bin/env python3
"""S146 aggregate of s146_sweep.jsonl."""
import json, collections
rows = [json.loads(l) for l in open('s146_sweep.jsonl')]
fails = [r for r in rows if 'FAIL' in r]
ok = [r for r in rows if 'FAIL' not in r]
print("instances", len(rows), "harness_failures", len(fails), "all_pass", sum(r['all_pass'] for r in ok))
for mode in ('thm', 'rnd'):
    sub = [r for r in ok if r['mode'] == mode]
    print(f"[{mode}] n_inst={len(sub)} pass={sum(r['all_pass'] for r in sub)} inner<=bound={sum(r['inner_dim']<=r['lemma_bound'] for r in sub)} inner==bound={sum(r['inner_dim']==r['lemma_bound'] for r in sub)}")
th = [r for r in ok if r['mode'] == 'thm']
byn = collections.defaultdict(list)
for r in th: byn[r['n']].append(r)
print("n | s | nq(range) | ell(range) | vxc_upper(range) | ratio/sqrt(n) max | vxc_upper<n ? | added3 count | ell<=2s+1")
for n in sorted(byn):
    rs = byn[n]
    f = lambda k: (min(r[k] for r in rs), max(r[k] for r in rs))
    print(n, rs[0]['s'], f('nq'), f('ell'), f('vxc_upper'), max(r['ratio_vxc_upper_sqrtn'] for r in rs),
          all(r['vxc_upper'] < n for r in rs), sum(r['added3'] for r in rs)//3, all(r['ell_le_2s_plus_1'] for r in rs))
print("first n with vxc_upper < n on all seeds:", min(n for n in byn if all(r['vxc_upper'] < n for r in byn[n])))
print("lambda* range (float, info only):", min(r['lambda_star_float'] for r in ok), max(r['lambda_star_float'] for r in ok))
print("brute-force Minkowski check run on", sum(1 for r in ok if 'brute_all_sums_in_R' in r['V2']), "instances, all true:", all(r['V2'].get('brute_all_sums_in_R', True) for r in ok))
