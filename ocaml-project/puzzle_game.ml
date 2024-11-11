let rec print_board n counter board=
  match board with
  | [] -> print_endline ""
  | h::t -> if h = 0 then print_string "   " else Printf.printf "%3d" h;
            if Int.equal (counter mod n) (n-1) then print_char '\n' else print_char ' ';
            print_board n (counter+1) t 

let rec check_power n m=
  if ((m*m) - 1) = n then m
  else if m > n then -1
  else check_power n (m+1) 

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
          let drawn_val = take_element idx 0 nmbrs in
          let new_nmbrs = remove_element idx 0 nmbrs in
          board_generator (drawn_val::board) new_nmbrs

let () =
  print_string "Enter the size of the puzzle:";
  let n = int_of_string (read_line ()) in
  let power = (check_power n 2) in
  Random.self_init ();
  if power >=0 then
    let nmbrs = build_nmbrs n [] in
    let board = (board_generator [] nmbrs) in
    print_board power 0 board
  else
    print_string "invalid input\n"
