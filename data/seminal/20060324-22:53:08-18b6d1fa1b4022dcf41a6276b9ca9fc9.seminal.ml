
exception Unimplemented
exception AlreadyDone

let twopi = 2.0 *. 3.14

(*** part a ***)
type move = Home | Forward of float
  | Turn of float | For of int * (move list)

(*** part b ***)
let makePoly sides len = 
  let fm = Forward(len) in
  let tm = Turn(twopi /. float_of_int sides) in
  For(sides,[fm;tm])

(*** part c ***)
let interpLarge (movelist : move list) : (float*float) list = 
  let rec loop movelist x y dir acc =
    match movelist with
      [] -> acc
    | Home::tl -> loop tl 0.0 0.0 0.0 ((0.0,0.0)::acc)
    | Forward(f)::tl -> 
	   let nx = (x +. f *. (cos dir)) in
	   let ny = (y +. f *. (sin dir)) in
	   loop tl nx ny dir ((nx,ny)::acc)
    | Turn(f)::tl -> loop tl x y (mod_float (dir +. f) twopi) acc
    | For(i,ml)::tl -> 
        if i > 0 
        then let nml = For((i-1),ml)::tl in
        loop (ml@nml) x y dir acc
        else loop tl x y dir acc
         
  in List.rev (loop movelist 0.0 0.0 0.0 [(0.0,0.0)])

(*** part d ***)
let interpSmall (movelist : move list) : (float*float) list = 
  let interpSmallStep movelist x y dir : move list * float * float * float = 
    match movelist with
      [] -> raise Unimplemented
    | Home::tl -> (tl,0.0,0.0,0.0)
    | Forward(f)::tl -> 
	   let nx = (x +. f *. (cos dir)) in
	   let ny = (y +. f *. (sin dir)) in
	   (tl,nx,ny,dir)
    | Turn(f)::tl -> (tl,x,y,(mod_float (dir +. f) twopi))
    | For(i,ml)::tl -> 
        if i > 0 
        then let nml = For((i-1),ml)::tl in
        ((ml@nml),x,y,dir)
        else (tl,x,y,dir)
  in
  let rec loop movelist x y dir acc =
    match movelist with
      [] -> acc
    | _ -> let(ml,xr,yr,dr) = (interpSmallStep movelist x y dir) in
      let accnew = 
        if xr=x && yr=y then acc else (xr,yr)::acc
      in
      loop ml xr yr dr accnew
  in 
  List.rev (loop movelist 0.0 0.0 0.0 [(0.0,0.0)])

(*** part e ***)

(* 
###########################################################################
###################################################################################################
################################################

###########
###############

###################################################################################################################

*)

(*** part f ***)
let rec tail lt =
  match lt with
    [] -> ()
  | (hd::[]) -> hd
  | (hd::tl) -> tail tl

let rec interpTrans movelist : float->float->float-> (float * float) list * float= 
  let compose f1 f2 = 
    (fun x y d -> 
      let (trl2,d2) = (f1 x y d) in
      if trl2 = [] 
      then (f2 x y d2)
      else  
        let (x2,y2) = (tail trl2) in
        let (trl3,d3) = (f2 x2 y2 d2) in
        ((trl2@trl3),d3))
  in
  match movelist with
    [] -> (fun x y d -> ([],d))
  | Home::tl -> 
    let ft = (interpTrans tl) in
    (fun x y d -> 
      if x=0.0 && y=0.0 
      then (ft 0.0 0.0 0.0)
      else let (rtl,d) = (ft 0.0 0.0 0.0) in
        ((0.0,0.0)::rtl,d))
  | Forward(f)::tl -> 
    let ft = (interpTrans tl) in
    (fun x y d -> 
      if f = 0.0
      then (ft x y d)
      else
        let nx = (x +. f *. (cos d)) in
	    let ny = (y +. f *. (sin d)) in
	    let (rtl,d) = (ft nx ny d) in
	    ((nx,ny)::rtl,d))
  | Turn(f)::tl -> 
    let ft = (interpTrans tl) in
    (fun x y d -> (ft x y (mod_float (d +. f) twopi)))
  | For(i,ml)::tl -> 
    let ft = (interpTrans tl) in
    let mlt = (interpTrans ml) in
    (fun x y d -> 
        let rec loopbody count = 
          if count = 0 
          then (ft)
          else (compose mlt (loopbody (count-1)))
        in
        (loopbody i x y d))
          

(*** possibly helpful testing code ***)

(* ######################################################################## *)
(* ############################################# *)
let example_logo_prog = [(makePoly 4 2.0);Home;(makePoly 3 4.0);Home;For(2,[Forward(1.0);Forward(1.0)])]
let ansL = interpLarge example_logo_prog
let ansS = interpSmall example_logo_prog
let ansI = (0.0,0.0)::(fst ((interpTrans example_logo_prog) 0.0 0.0 0.0))

let rec pr lst =
  match lst with
    [] -> ()
  | (x,y)::tl -> 
      print_string("(" ^ (string_of_float x) ^ "," ^ (string_of_float y) ^ ")");
      pr tl

let _ = 
  pr ansL; print_newline (); 
  pr ansS; print_newline ();
  pr ansI; print_newline (); 
