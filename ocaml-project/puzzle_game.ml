let get_2d idx_1d n=
  let x = (idx_1d mod n) in
  let y = (idx_1d / n) in
  [|x;y|]

let get_1d idxs_2d n=
  (idxs_2d.(0)+idxs_2d.(1)*n)

let rec print_horizontal_line counter n =
  if counter=(n*4+1) then print_string "-\n"
  else begin print_char '-'; print_horizontal_line (counter+1) n end

let rec print_board n counter board=
  if counter=0 then begin (print_horizontal_line 0 n); print_char '|'; end else ();
  match board with
  | [] -> print_char '\b'; print_horizontal_line 0 n; print_endline ""
  | h::t -> if h = 0 then print_string "   " else Printf.printf "%3d" h;
            if Int.equal (counter mod n) (n-1) then print_string " |\n|" else print_char ' ';
            print_board n (counter+1) t 

let rec build_nmbrs n nmbrs=
  match n with
  | 0 -> (n::nmbrs)
  | _ -> build_nmbrs (n-1) ((n)::nmbrs)

let rec take_element idx counter nmbrs =
  match nmbrs with
  | [] -> -1
  | h::t -> if idx=counter then h else take_element idx (counter+1) t 

let rec remove_element idx counter nmbrs =
  match nmbrs with
  | [] -> []
  | h::t -> if idx=counter then remove_element idx (counter+1) t 
    else h::remove_element idx (counter+1) t

let rec board_generator board nmbrs =
  match nmbrs with
  | [] -> board
  | _ ->  let nmbrs_length = List.length nmbrs in
          let idx = Random.int nmbrs_length in
          (* take element of the randomly generated idx *)
          let drawn_val = take_element idx 0 nmbrs in
          (* removes the taken elemnt from the remainging numbers *)
          let new_nmbrs = remove_element idx 0 nmbrs in
          (* add taken element to the board *)
          board_generator (drawn_val::board) new_nmbrs

let rec switch_elements switch_number board = 
  match board with 
  | [] -> []
  | h::t -> if h = 0 then switch_number::switch_elements switch_number t 
  else if h = switch_number then 0::switch_elements switch_number t
  else h::switch_elements switch_number t

let rec final_state board size counter =
  match board with
  | [] -> true
  | h::t -> if h = counter then final_state t size (counter+1) 
            else if h = 0 && counter = size then true
            else false

let rec get_idx number counter board =
  match board with
  | [] -> -1
  | h::t -> if h=number then counter else get_idx number (counter+1) t

let check_move zero_idxs movement n board =
  let other_idxs =
    match movement with
    |"w" -> [|zero_idxs.(0); (zero_idxs.(1)+1)|]
    |"s" -> [|zero_idxs.(0); (zero_idxs.(1)-1)|]
    |"a" -> [|(zero_idxs.(0)+1); zero_idxs.(1)|]
    |"d" -> [|(zero_idxs.(0)-1); zero_idxs.(1)|]
    | _ -> [|zero_idxs.(0); zero_idxs.(1)|]
    in
    if ((other_idxs.(0)>=0) && (other_idxs.(1)>=0)) && ((other_idxs.(0)<n) && (other_idxs.(1)<n)) then 
    let switch_number = (take_element (get_1d other_idxs n) 0 board) in
      switch_elements switch_number board
    else
      board

let invert_movement h=
  if h = "w" then "s"
  else if h="s" then "w"
  else if h="d" then "a"
  else "d"

let rec manhattan_distance board counter n sum=
  let calculate_one_distance idx nmbr=
    let should_be_idxs_2d = get_2d (nmbr-1) n in
    let idxs_2d = get_2d idx n in
    abs (should_be_idxs_2d.(0)-idxs_2d.(0)) + abs (should_be_idxs_2d.(1) - idxs_2d.(1))
  in
  match board with
  | [] -> sum
  | h::t -> if h = 0 then manhattan_distance t (counter+1) n sum
            else manhattan_distance t (counter+1) n (sum+(calculate_one_distance counter h))


let rec play_game board size n moves_taken=
  if final_state board size 1 = false then begin
    print_string "which direction you want to move? Left (a), right(d), up (w), down (s)";
    let choice = read_line () in 

    let movement = 
      if choice = "u" then 
      match moves_taken with
      | [] -> "x"
      | h::t -> invert_movement h
      else
      choice
    in

    let new_moves_taken = 
      if choice = "u" then 
      match moves_taken with
      | [] -> moves_taken
      | h::t -> t
      else
      choice::moves_taken
    in

    let zero_idx = get_idx 0 0 board in 
    let updated_board = check_move  (get_2d zero_idx n) movement n board in
    print_board n 0 updated_board;
    print_int (manhattan_distance updated_board 0 n 0);
    play_game updated_board size n new_moves_taken
    end
  else
    print_endline "you won the game, congratulations!"
(* why () *)

let () =
  print_string "Enter the size of the puzzle:";
  let n = int_of_string (read_line ()) in
  if (n > 1) then
    (* makes a list with numbers 0-n *)
    let nmbrs = build_nmbrs (n*n-1) [] in
    (* genertates board *)
    let board = (board_generator [] nmbrs) in
    print_board n 0 board; 
    play_game board (n*n) n []
    (* take movement from user input *)
  else
    print_string "Invalid input\n"
