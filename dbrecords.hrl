-define(MFAMagicCode, letmego).
-record(employee,{emp_no,   %Emploree id
		  name,     %Emploree Name
		  card_num, %Emploree Card Number
		  last_record_num, %Last record that emploree input
		  last_check_in, %Last time that emploree checked in
		  title, %Title of emploree
		  salary}). %Salary of emploree

-record(workRecord,{index,
		    time,
		    emp_no,
		    product,
		    process,
		    machine,
		    shift,
		    parms
		   }).

-record(colMap,{attrName,
		status
	 }).
