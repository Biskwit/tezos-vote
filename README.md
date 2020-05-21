# tezos-vote

## Compile contract

```bash
ligo compile-contract vote.ligo main > vote.tz
```

```bash

contract.ligo :

ligo compile-storage vote.ligo main 'record[pause = True; oui = 0n; non = 0n; voters = (Set.empty : set(address))]'

```

## Dry-run

```bash

ligo dry-run --source="tz1fdtrrRmVFA1xGLgKi33UqT9LjQRZneXrc" vote.ligo main 'Vote(1n)' 'record[pause = True; oui = 0n; non = 0n; voters = (Set.empty : set(address))]'

ligo dry-run --source="tz1fdtrrRmVFA1xGLgKi33UqT9LjQRZneXrc" vote.ligo main 'Break("True")' 'record[pause = True; oui = 0n; non = 0n; voters = (Set.empty : set(address))]'

```

## Tests unitaires

```bash

pytest tests.py

```
