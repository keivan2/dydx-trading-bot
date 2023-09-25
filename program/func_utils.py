# Fomrat number
def format_number(curr_num, match_num):
    # Give current number an example of number with decimals desired
    # function will return the correctly formatted string

    curr_num_string = f"{curr_num}"
    match_num_string = f"{match_num}"

    if "." in match_num_string:
        match_decimals = len(match_num_string.split(".")[1])
        # Second f for format, match curr_num with match_num
        curr_num_string = f"{curr_num:.{match_decimals}f}"
        curr_num_string = curr_num_string[:]
        return curr_num_string
    else:
        return f"{int(curr_num)}"
