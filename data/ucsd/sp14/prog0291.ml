
let rec digitsOfInt n =
  if n <= 0 then [] else (match n with | n -> [] @ (n mod 10));;