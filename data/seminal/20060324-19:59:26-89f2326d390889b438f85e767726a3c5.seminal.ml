
exception Unimplemented
exception AlreadyDone

(*** part a ***)
type move = Home | Forward of float
 	    | Turn of float | For of int * (move)list


(*** part b -- return move***)
let makePoly sides len =
  let fSides = float_of_int sides in
  let turnAmount = (2.0 *. 3.1416) /. fSides in
  let rec makePolyHelp sidesLeft turn =
    match sidesLeft with
      0 -> []
    | 1 -> [Home](*::makePolyHelp 0 true*)
    | _ -> 
        (Forward(len)::[Turn(turnAmount)])
(*
######################
#############
########################################################
############
#########
#############################################
################################################
######
*)
  in
  if sides < 3
  then
    For(0, [])
  else
  (
    let lst = makePolyHelp sides false in
    For(sides, lst)
  )
  
(*** part c ***)
let interpLarge (movelist : move list) : (float*float) list = 
  let rec loop movelist x y dir acc =
    match movelist with
      [] -> acc
    | Home::tl -> loop tl 0.0 0.0 dir ((0.0,0.0)::acc)
    | Forward f::tl -> 
          let newX = x +. ( f *. (cos dir) ) in
          let newY = y +. ( f *. (sin dir) ) in
          loop tl newX newY dir ((newX,newY)::acc)
    | Turn f::tl -> 
          let newDir = f +. dir in
          loop tl x y newDir acc
    | For (il, ml)::tl -> 
          if il > 0
          then
            let ild = il - 1 in
            let newMlTemp = For(ild, ml)::tl in
            let newMl = List.append ml newMlTemp in
            loop newMl x y dir acc
          else  
            loop tl x y dir acc
  in List.rev (loop movelist 0.0 0.0 0.0 [(0.0,0.0)])
 
(*** part d ***)
let interpSmall (movelist : move list) : (float*float) list = 
  let interpSmallStep movelist x y dir : move list * float * float * float = 
  match movelist with
    [] -> print_string "[]";print_newline ();raise AlreadyDone
  | Home::tl -> tl, 0.0, 0.0, 0.0
  | Forward f::tl -> 
          let newX = x +. ( f *. (cos dir) ) in
          let newY = y +. ( f *. (sin dir) ) in
          tl, newX, newY, dir
  | Turn f::tl -> 
          let newDir = f +. dir in
          let radianCirc = 2.0 *. 3.1416 in
          let newDirNor = mod_float newDir radianCirc in
          tl, x, y, newDirNor
  | For (il, ml)::tl -> 
          if il > 0
          then
          (
            let ild = il - 1 in
            let newMlTemp = For(ild, ml)::tl in
            let newMl = List.append ml newMlTemp in
            newMl, x, y, dir
          )
          else
            tl, x, y, dir
  in
  let rec loop movelist x y dir acc =
    match movelist with
      [] -> acc
    | _  ->
          let ret = interpSmallStep movelist x y dir in
          match ret with
            newList, retX, retY, retDir ->
                  if retX <> x || retY <> y
                  then
                    loop newList retX retY retDir ((retX, retY)::acc)
                  else
                    loop newList x y retDir acc
  in
    List.rev (loop movelist 0.0 0.0 0.0 [(0.0,0.0)]) 

(*** part e ***)

(* 
######################################################################
#############################################################################
##########################################
*)

(*** part f ***)
let interpTrans movelist : float->float->float-> (float * float) list * float= 
  let compose f1 f2 = raise Unimplemented (* ######################### *)
  in
  
  let transMatch movelistMatch x y dir = 
  match movelistMatch with
    [] -> -1.0, -1.0, -999.0, []
  | Home::tl -> 0.0, 0.0, 0.0, tl
  | Forward f::tl -> 
        let newX = x +. ( f *. (cos dir) ) in
        let newY = y +. ( f *. (sin dir) ) in
        newX, newY, dir, tl
  | Turn f::tl -> 
        let newDir = f +. dir in
        x, y, newDir, tl
  | For (il, ml)::tl -> 
        print_int il;
        print_string "___";
        if il > 0
        then
        (
          let ild = il - 1 in
          let newMlTemp = For(ild, movelistMatch)::tl in
          let newMl = List.append ml newMlTemp in
          x, y, dir, newMl
        )
        else
          x, y, dir, tl
        
  in

  let loop movelist = 
    (fun x y dir -> 
      let rec loopHelp movel x y dir acc = 
        let res = transMatch movel x y dir in
          match res with 
            -1.0, -1.0, -999.0, _ -> acc, dir
          | retX, retY, retDir, tl       -> 
              if retX <> x || retY <> y
              then
              (
                let lst = [(retX,retY)] in
                let newAcc = List.append acc lst in
                loopHelp tl retX retY retDir newAcc
              )
              else
              (
                if retDir <> dir
                then
                  loopHelp tl retX retY retDir tl
			    else
			      loopHelp tl retX retY dir tl
              )
      in  
      loopHelp movelist x y dir []  ) 
  in  
  loop movelist


(*** possibly helpful testing code ***)

(* ######################################################################## *)
(* ############################################# *)
let example_logo_prog = 

  let res = makePoly 5 1.0 in
  [res]
(*

###############################
##################################
######################
*)  
  
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

