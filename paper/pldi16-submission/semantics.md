# Type-Carrying

## Syntax

```
E ::= V
   |  E E
   |  \X -> E
   |  if E then E else E
   |  E + E

V ::= N
   |  B
   |  _ : T
   |  stuck T T

T ::= bool
   |  nat
   |  a
```

- probably want to add datatypes
- do we want to deal with env-passing in the description? or leave as implementation detail?

## Semantics

### relies on `force` and `gen` helpers

```
gen : T -> V
gen int  = N
gen bool = B
gen a    = _ : a

force : V -> T -> V
force N int
  = N
force N t
  = stuck int t
force B bool
  = B
force B t
  = stuck bool t
force (_ : t1) t2
  | unify t1 t2
  = gen t2
  | otherwise
  = stuck t1 t2
```

### Important single-step rules

```
v1 + v2
~>
[[force v1 nat + force v2 nat]]

if v1 then e1 else e2, true = force v1 bool
~>
e1

if v1 then e1 else e2, false = force v1 bool
~>
e2

if v1 then e1 else e2, stuck t1 t2 = force v1 bool
~>
if stuck t1 t2 then e1 else e2

(\x -> e) v
~>
e[x/v]
```

- note that we can get only get stuck at "primitive" operations
- beta-reduction *does not* type-check the argument


- HOW DO YOU FORMALIZE "no false positives"??

- make a lattice of types?
  - what is the edge relation?

- failing "as late as possible"
  - given a path through CFG that crashes at location 't'
  - there is no input that goes beyond 't'
  - t < t'
