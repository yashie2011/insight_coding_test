import sys
import argparse
import itertools

LIST_SIZE = 3

# to check if the given string is a number
def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True

#read actual file or predicted file and return a list of dicts {stock, value} for each hour
def read_actual_predict(filename):
	prev_hour = 0
	stock_dict_list=[]  # list of dictionaries representing <{stock:value}>
	stock_dict = {} # dictionary {stock:value} for each hour
	


	# Open a file and read each line
	with open(filename) as fp:
		for line in fp:
			piped_str = line.rstrip('\n')
			stock_list = piped_str.split('|')
			
			#check if the line is correct in the text
			if(len(stock_list) != LIST_SIZE):
				raise ValueError("the input list is not in correct format")
			else:
				#check if the hour and stock value are numbers
				if not stock_list[0].isdigit() and not is_number(stock_list[2]):
					raise ValueError("the first character in the input string is not an integer number")
				else:
					# create a dictionary for each hour and store key value pairs of stock and values
					if int(stock_list[0]) == prev_hour: 
						stock_dict[stock_list[1]] = float(stock_list[2])
					elif int(stock_list[0]) > prev_hour:
						if prev_hour > 0:
							stock_dict_list.append(stock_dict)
						prev_hour = int(stock_list[0])
						stock_dict = {}
						stock_dict[stock_list[1]] = float(stock_list[2])
					else:
						raise ValueError("incorrect order of time")
						
		stock_dict_list.append(stock_dict)
		print "read the "+ filename +" stock file: "+str(len(stock_dict_list))+" hours"
		return stock_dict_list
					


# give two dicts, it returns a list of errors					
def dict_diff(st_d1, st_d2):
	err_list = []
	for key in st_d1:
		if key in st_d2:
			err = abs(st_d1[key]-st_d2[key])
			err_2f = float("%0.2f"%err)
			err_list += [err_2f]
	
	return err_list



# write the error list of the sliding window to the output file
def write_error(count, win, error_list, output_filename):
	
	# check if the error list is not empty
	if len(error_list) > 0:
		avg_err = float("%0.2f"%(sum(error_list)/float(len(error_list))))
	else:
		raise ValueError("Error list is empty")
	
	#create a string to output to the file	
	compare_str = str(count+1)+"|"
	compare_str += str(count+win)+"|"
	compare_str += str(avg_err)
	
	# open a file, and append it to the output
	with open(output_filename, 'a') as wf:
		wf.write(compare_str+"\n") 
		


# compare the actual, and predicted lists, and output the difference into a filename
def compare_predict(act_list, pred_list, win, output_filename):
	
	# checks if the window length is greater than hours in input texts
	if win > len(act_list) or win > len(pred_list):
		raise ValueError("window size is greater than hours in input texts")
	
	# checks if actual and predicted files have same number of hours
	if len(act_list) != len(pred_list):
		raise ValueError("lists of different sizes")
	else:
		count = 0
		error_list = []
		length = len(act_list)
		
		# for each hour in the text file compute error
		while count <= length-win+1:
			inner_count = 1
			error_list = []
			
			# implement sliding window
			for act_st_d, pred_st_d in itertools.izip(act_list, pred_list):
				error_list += dict_diff(act_st_d, pred_st_d)
				
				if inner_count == win:
					write_error(count,win, error_list, output_filename)
					break
				else:
					inner_count += 1
			count += 1
			
			# delete the top most element to move to the next hour
			if len(act_list) > 0 and len(pred_list) > 0:
				del act_list[0]
				del pred_list[0]



# reads window file and gives out the sliding window time
def read_window(filename):
	with open(filename) as fp:
		for line in fp:
			if line.rstrip('/n').isdigit:
				return int(line.rstrip('/n'))
			else:
				raise ValueError("Incorrect value in window file")




# Driver function to process each file and call the compare code
def test_main(act_file, pred_file, window, output_filename):
	act_list = []
	pred_list = []
	win = 1
	try:
		act_list = read_actual_predict(act_file)
	except ValueError as err:
		print(err)
	try:	
		pred_list = read_actual_predict(pred_file)
	except ValueError as err:
		print(err)
	try:
		win = read_window(window)
	except ValueError as err:
		print (err)
	try:
		compare_predict(act_list, pred_list, win, output_filename)
	except ValueError as err:
		print(err)
		
		
	
if __name__ == "__main__":
	
	# parse the input arguments that are passed from run.sh
	parser = argparse.ArgumentParser()
	parser.add_argument("window", help = "file containing the window duration")
	parser.add_argument("actual_text", help = "file containing the actual stock values")
	parser.add_argument("pred_text", help = "file containing the predicted stock values")
	parser.add_argument("outfile", help = "file to out the comparison")
	args = parser.parse_args()
	
	# call the code that computes error on the data
	test_main(args.actual_text, args.pred_text, args.window, args.outfile)
	
