#!/bin/bash
# S146 sweep: theorem construction and random-Q lemma generality. Output: JSONL.
cd "$(dirname "$0")"
OUT=s146_sweep.jsonl; : > $OUT
for n in 9 10 16 25 36 49 50 64 100 101 144 150 196 256 400; do
  for seed in 1 2 3; do timeout 900 python3 s146_vxc.py thm $n $seed >> $OUT || echo "{\"FAIL\":\"thm $n $seed\"}" >> $OUT; done
done
for n in 20 50 100; do for K in 3 5 8 12; do for seed in 1 2; do
  timeout 900 python3 s146_vxc.py rnd $n $seed $K >> $OUT || echo "{\"FAIL\":\"rnd $n $seed $K\"}" >> $OUT
done; done; done
echo DONE >> s146_sweep.done
