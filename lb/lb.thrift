
service LBSvc { 
 # Get last N lines. This service is added for the fault recovery.
 list<string> get_lines(1:i32 n),

 # Shrink file by 'n' number of lines and 
 void shrink_file(1:i32 n, 2:i32 num_lines),

 # Prepend file by 'n' number of lines
 void prepend_file(1:list<string> lastNlines),

 # Shrink file on server A and prepend file on server B 
 void load_balance(1:i32 n, 2:i32 b_port),
}
