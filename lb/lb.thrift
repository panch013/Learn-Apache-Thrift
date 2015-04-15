
service LBSvc { 
 # Shrink file by 'n' number of lines and 
 # return those lines
 list<string> shrink_file(1:string file_, 2:i32 n),
 # Prepend file by 'n' number of lines
 void prepend_file(1:string file_, 2:list<string> lastNlines),
 # Shrink file on server A and prepend file on server B 
 void load_balance(1:i32 a_po, 3:i32 n, 4:i32 b_port, 5:string b_file),
}
