let rec print_board n counter board=
  match board with
  | [] -> print_endline ""
  | h::t -> if h = 0 then print_string "   " else Printf.printf "%3d" h;
            if Int.equal (counter mod n) (n-1) then print_char '\n' else print_char ' ';
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

let rec switch_elements zero switch_number board = 
  match board with 
  | [] -> []
  | h::t -> if h = zero then switch_number::switch_elements zero switch_number t 
  else if h = switch_number then zero::switch_elements zero switch_number t
  else h::switch_elements zero switch_number t

let rec get_idx number counter board =
  match board with
  | [] -> -1
  | h::t -> if h=number then counter else get_idx number (counter+1) t

let check_move zero_idx offset n board =
  let new_idx = zero_idx + offset in
  if new_idx >= 0 && new_idx < n * n &&
      ((offset = -1 &&  (zero_idx / n) = (new_idx / n)) || (* Left *)
      (offset = 1 &&  (zero_idx / n) = (new_idx / n)) || (* Right *)
      ((offset = -n) && (zero_idx mod n) = (new_idx mod n))|| (* Up *)
      ((offset = n) &&  (zero_idx mod n) = (new_idx mod n)))(* Down *)
  then
    let switch_number = take_element new_idx 0 board in
    switch_elements 0 switch_number board
  else
    (print_string "Move not possible\n"; board)

(* why () *)
let () =
  print_string "Enter the size of the puzzle:";
  let n = int_of_string (read_line ()) in
  let total_amount = n*n - 1 in  
  Random.self_init ();
  if total_amount >=0 then
    (* makes a list with numbers 0-n *)
    let nmbrs = build_nmbrs total_amount [] in
    (* genertates board *)
    let board = (board_generator [] nmbrs) in
    print_board n 0 board; 
    (* take movement from user input *)
    print_string "which direction you want to move? Left (l), right (r), up (u), down (d)";
    let movement = read_line () in 
    let zero_idx = get_idx 0 0 board in 
    let updated_board = 
      match movement with 
      | "l" -> check_move zero_idx (1) n board
      | "r" -> check_move zero_idx (-1) n board
      | "u" -> check_move zero_idx (n) n board
      | "d" -> check_move zero_idx (-n) n board
      | _ -> (print_string "Not a valid move"; board)
    in
    print_board n 0 updated_board
  else
    print_string "Invalid input\n"


    (* if movement = "l" then 
      if (zero_idx / n) = ((zero_idx + 1) / n) && zero_idx + 1 < n*n then 
        let switch_number = take_element (zero_idx+1) 0 board in 
        let board = switch_elements 0 switch_number board in 
        board 
      else (print_string "Move not possible"; board);
    else if movement = "r" then 
      if (zero_idx / n) = ((zero_idx - 1) / n) && zero_idx - 1 > -1 then 
        let switch_number = take_element (zero_idx-1) 0 board in 
        let board = switch_elements 0 switch_number board in 
        board 
      else (print_string "Move not possible"; board);
    else if movement = "u" then 
      if (zero_idx mod n) = ((zero_idx - n) mod n) && zero_idx - n > -1 then 
        let switch_number = take_element (zero_idx-n) 0 board in 
        let board = switch_elements 0 switch_number board in 
        board 
      else (print_string "Move not possible"; board);
    else if movement = "d" then 
      if (zero_idx mod n) = ((zero_idx + n) mod n) && zero_idx + n < n*n then 
        let switch_number = take_element (zero_idx+n) 0 board in 
        let board = switch_elements 0 switch_number board in 
        board 
      else (print_string "Move not possible"; board)
    else print_string "not a valid move";
    print_board n 0 board 
  
  else
    print_string "invalid input\n";
  *)
(* let return_1d x y n = 
  if y * n + x > -1 & y * n + x < n * n then y * n + x else print_string "invalid input\n"; *)



  (* print_string "Enter column of number you want to move";
  let x = int_of_string (read_line ()) in
  print_string "Enter row of number you want to move";
  let y = int_of_string (readline ()) in 
  let place_in_board = return_1d x y n in  *)
 

