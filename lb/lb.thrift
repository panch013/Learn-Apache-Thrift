
service LBSvc { 
 # Get last N lines. This service is added for the fault recovery.
 list<string> get_lines(1:i32 n),

 # Get File in binary format
 binary get_file(1:i32 n),

 # Shrink file by 'n' number of lines 
 void shrink_file(1:i32 n, 2:i32 num_lines),

 # Prepend file by 'n' number of lines using list
 void prepend_file_list(1:list<string> lastNlines),
 
 # Prepend file by 'n' number of lines using binary
 void prepend_file(1:binary lastNlines_bin),

 # Shrink file on server A and prepend file on server B 
 void load_balance(1:i32 n, 2:i32 b_port),
}
