import Lake
open Lake DSL

package geometry

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.32.0"

@[default_target]
lean_lib Orthogenesis
