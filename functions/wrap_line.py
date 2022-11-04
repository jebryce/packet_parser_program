# this is used to wrap long strings when printing. 
#
# Ideally it breaks the string into 2 (or more) strings at a space, if not, 
# then it hypenates
#
# returns return_list, which you need to provide when calling (should provide 
# an empty list)
#
# also provide the string you would like to break up and the maximum length 
# (variable: cutoff) of strings you would like returned
def wrap_line(return_list, string, cutoff):
    # removes whitespace from start and end of string
    string = string.strip()


    # find the index of the first space character
    if len(string) <= cutoff:
        # this is a recursive program, so once it has finished breaking the 
        # string up, this is how it finishes
        return_list.append(string)
    else:
        # so if cutoff = 9 (realistically the cutoff should be much higher)
        # Takes the first 10 characters of string (reason this is done is if a 
        # space is the 10th character, as described below)
        line = string[:cutoff+1]
        # then reverses
        reversed_line = line[::-1]
    
        # finds where first space is, if no spaces then return -1
        index = reversed_line.find(' ')
        if index == 0:
            # space character has been found right after the cutoff
            # so if cutoff = 50, and there is a space at location 51, then we 
            # want to return a string that is 50 characters long, then have the 
            # next word start in the next string to be returned
            #
            # If this wasn't implemented, say cutoff = 9:
            # and the string was: 'hello you there man' 
            # then it would return ['hello','you there','man]
            # instead of: ['hello you','there man']
            return_list.append(line.strip())
            wrap_line(return_list,string[cutoff-index:],cutoff)
        elif index != -1:
            # space character has been found within cutoff
            #
            # ex: if cutoff is 9 and string is 'kittens are cute'
            # then return ['kittens', 'are cute']
            return_list.append(reversed_line[index:][::-1].strip())
            wrap_line(return_list,string[cutoff-index:],cutoff)
        else:
            # this would be if there isn't a space, then a hypen needs to be put
            # ex: if cutoff is 9 and the string is 'laboratories'
            # return ['laborato-','ries'] 
            return_list.append(line[:cutoff-1]+'-')
            wrap_line(return_list,string[cutoff-1:],cutoff)
            
    
    return return_list