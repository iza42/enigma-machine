import sys
import os


def take_key_matrix(path):
    """First checks if the path exists if not raises an error,then check for if the path ends with txt(so we can read it) if not
    raises an error again. Then reads the file ; if the file is empty raises an error, if not empty but has unallowed characters raises an error, if has allowed characters
    but has a wrong format(not square matrix) raises an error. If the all the conditions is okay, then reads the file and returns the matrix and length of the matrix."""

    assert os.path.exists(path) , "The path for key file is not exist."

    assert path.endswith(".txt") ,"Key file could not be read. Key file path should end with(.txt)."

    with open(path, "r") as file:
        info_list= file.readlines()
        file.seek(0)
        info_str=file.read()

        assert (len(info_str)!=0) , "Key file is empty."

        for i in [i.replace("\n", "").split(",") for i in info_list]:
            for j in i:
                # when the number is minus or when there are characters that are not allowed
                assert j.isnumeric() , "Invalid character in key file:only allowed positive numbers and comma."

        for li in [element.split(",") for element in info_list]:
            list1 = []
            for ki in li:
                list1.append(ki)
                if ki == "\n" or ki == "":
                    list1.remove(ki)
            # we look at whether the given key matrix is square
            assert (len(list1) == len(info_list)) , "Invalid content for key file, the given key matrix must be square"

        for el in [element.split(",") for element in info_list]:
            for e in el:
                assert (len(e) !=0) ,"Invalid content for key file, there is more than one comma between the numbers."

        size=len(info_list) # size of the key matrix : nxn
        info_ = [eleman.replace("\n", "") for eleman in info_list]  # we deleted the newline characters
        liste = [i.split(",") for i in info_]  # separated the numbers(still str) by comma
        key_matrix = []
        for sublist in liste:
            key_matrix.append(list(map(int, sublist)))  # we have converted the values that are str into integers
        return key_matrix ,size



def translate_dictionary():
    """It holds the dictionary that we use for encoding"""
    translate = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
                 "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19,
                 "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26, " ": 27}
    return translate
def reverse_dictionary(dictionary):
    """It returns the dictionary that we use for decoding"""
    return {value: key for key, value in dictionary.items()}
def convert_plain_input_to_matrix(path,dictionary,key_matrix_size):
    """First checks if the path exists if not raises an error,then check for if the path ends with txt(so we can read it) if not
       raises an error again. Then reads the file ; if the file is empty raises an error, if not empty but has unallowed characters raises an error. If the all
       the conditions is okay, then reads the file and returns the matrix."""

    assert os.path.exists(path) , "The path for input file is not exist."

    assert path.endswith(".txt") ,"The input file could not be read. The input file path should end with(.txt)."

    with open(path, "r") as f:
        info_str = f.read()

        assert (len(info_str)!=0) , "Input file is empty."

        for i in info_str.upper():
            assert (i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ ") , "Invalid character in input file. Your file should only contain 26 characters in alphabet and space."

        f.seek(0)

        message_matrix = []
        if len(info_str) % key_matrix_size == 0:  # if the message length fits exactly into the key matrix size,if it can be divided by
            for i in range(int(len(info_str) / key_matrix_size)):
                small_group = []
                for j in range(1):
                    small_group.append(f.read(key_matrix_size))
                message_matrix.append(small_group)
        else:
            for i in range(int(len(info_str) / key_matrix_size) + 1):
                small_group = []
                for j in range(1):
                    small_group.append(f.read(key_matrix_size))
                message_matrix.append(small_group)
            message_matrix[int(len(info_str) / key_matrix_size)][0] += " " * (
                    key_matrix_size - (len(info_str) % key_matrix_size))  # if there's any remaining, add space

        mother_message_matrix = []
        for substr in [list(i) for element in message_matrix for i in element]:
            sub = []
            for letter in substr:
                if letter.upper() in dictionary:
                    sub.append(dictionary[letter.upper()])
            mother_message_matrix.append(sub)

        return mother_message_matrix


def operabilitiy(matrix):
    """Function prepare the matrix before the multiplication. Returns the new matrix that ready for multiplication."""
    for i in matrix:
        for idx, k in enumerate(i):
            i[idx] = [k]
    return matrix
def multiply_key_with_input(key_matrix,mother_matrix):
    """This function multiplies the given 2 matrix and returns the resultant matrix."""
    matrix = []
    for matrix2 in mother_matrix:
        result = [[0], [0]]
        for g in range(len(key_matrix)):
            for h in range(len(matrix2[0])):
                for p in range(len(matrix2)):
                    result[g][h] += key_matrix[g][p] * matrix2[p][h]
        matrix.append(result)
    return matrix


def write_for_enc(output_name,multiplied_matrix):
    """Function first looks for if there's a path that exist, if not throws an error. Then if the path exist but
    the path has a write protected path throws an error again. If everything was okay, function writes the encoded message to the file. """
    # If the path for output file is not exist, throw an error (this is what i understand from the assignment sheet)
    assert  os.path.exists(output_name) ,"Output file could not be written:The path is not exist."

    assert output_name.endswith(".txt") , "Output file could not be written:The file should end with(.txt)."

    with open(output_name, "w+") as f:
        writing = ""
        for n in multiplied_matrix:
            for m in n:
                for d in m:
                    writing += f"{d},"
        info1 = writing.rstrip(",")
        f.write(info1)


def write_for_dec(output_name, writing):
    """Function first looks for if there's a path that exist, if not throws an error. Then if the path exist but
       the path has a write protected path throws an error again. If everything was okay, function writes decoded message to the file. """
    assert  os.path.exists(output_name) ,"Output file could not be written:The path is not exist."

    assert output_name.endswith(".txt") , "Output file could not be written:The file should end with(.txt)."

    with open(output_name, "w+") as file:
        file.write(writing + "\n")



def matrix_to_text_for_dec(multiplied_matrix):
    """This function convert the decoded matrix to the message that was needed for the second world war.
    Returns that message."""
    writing = ""
    for n in multiplied_matrix:
        for m in n:
            for d in m:
                writing += f"{d},"
    only_numbers = writing.rstrip(",").split(",")
    only_numbers2=[int(float(i)) for i in only_numbers]
    list1 = []
    for number in only_numbers2:
        assert type(number)==int , "ValueError: something wrong with matrix multiplication."
        if int(number) in reverse_dictionary(translate_dictionary()):
            list1.append(reverse_dictionary(translate_dictionary())[int(number)])
    return ''.join(letter for letter in list1)

def convert_ciphertext_to_matrix(path, key_matrix_size):
    """First checks if the path exists if not raises an error,then check for if the path ends with txt(so we can read it) if not
       raises an error again. Then reads the file ; if the file is empty raises an error, if not empty but has unallowed characters raises an error. If the all
       the conditions is okay, then reads the decoded message from the file and convert it to a matrix. Returns that matrix."""
    assert os.path.exists(path) ,"The path for input file is not exist."

    assert path.endswith(".txt"), "The input file could not be read. Input file path should end with(.txt)."

    with open(path, "r") as file:
        info_str=file.read()
        info_list = info_str.split(",")

        assert (len(info_str) != 0) , "Input file is empty."

        for element in info_list:
            assert element.isnumeric() , "Invalid character in input file. Your file should only contain positive integers and comma."

        info1 = [int(t) for t in info_list]
        mother_decode_matrix = []
        for f in range(int(len(info1) / key_matrix_size)):
            mother_decode_matrix.append(info1[f * key_matrix_size:(f + 1) * key_matrix_size])
    return mother_decode_matrix



def Filenotfoundforinput(input_path):
    """This function specifically designed for looking if the input file is found or not at the given path.
    If the file is not found function returns the error message."""
    try:
        with open(input_path, "r") as file:
            file.read()
    except FileNotFoundError:
        return "Input file not found."
    except UnicodeError :
        return "The input file could not be read due to unicode error."
    except PermissionError:
        return "The input file could not be read due to permission error."




def filenotfoundforkey(key_path):
    """This function specifically designed for looking if the key file is found or not at the given path.
      If the file is not found function returns the error message."""
    try:
        with open(key_path, "r") as file:
            file.read()
    except FileNotFoundError:
        return "Key file not found."
    except UnicodeError:
        return "Key file could not be read due to unicode error."
    except PermissionError:
        return "Key file could not be read due to permission error."

def unit_matrix(size):
    """produces a unit matrix for the given size."""
    unit_matrix=[]
    for i in range(size):
        row = []
        for j in range(size):
            row.append(0)
        unit_matrix.append(row)
    for a in range(size):
        unit_matrix[a][a] = 1
    return unit_matrix

def matrix_multiply_number(matrix,number):
    """multiplies the every number in the matrix with the given number as an argument."""
    return [[matrix[u][p]*number for p in range(len(matrix))] for u in range(len(matrix))]

def liste_operator_number(list1,operator,number):
    """multiplies the every number in the list with the given number as an argument."""
    if operator =="+":
        return [(i+number) for i in list1]
    elif operator=="-":
        return [(i-number) for i in list1]
    elif operator=="*":
        return [(i*number) for i in list1]
    elif operator=="/":
        return [(i/number) for i in list1]

def add_onelist_scalarmultiple_theanother(list1,list2,multiplying_element):
    for element1,element2,i in zip( list1,list2,list(range(len(list2)))):
        list2[i]=element1*multiplying_element+element2
    return list2

def first_operation(real_matrix,unit_matrix): # makes zero the lower triangle
    for yi in range(len(real_matrix)-1):
        first_number = real_matrix[yi][yi]
        for ki in range(yi+1, len(real_matrix)):
            multiplying_element = round(-(real_matrix[ki][yi] / first_number),2)
            real_matrix[ki] = add_onelist_scalarmultiple_theanother(real_matrix[yi], real_matrix[ki], multiplying_element)
            unit_matrix[ki] = add_onelist_scalarmultiple_theanother(unit_matrix[yi], unit_matrix[ki], multiplying_element)
    return real_matrix,unit_matrix

def second_operation(real_matrix,unit_matrix): #makes one the diagonal(left to right)
    for i in range(len(real_matrix)):
        multiplying_element=round((1/real_matrix[i][i]),2)
        real_matrix[i]=liste_operator_number(real_matrix[i],"*",multiplying_element)
        unit_matrix[i]=liste_operator_number(unit_matrix[i],"*",multiplying_element)
    return real_matrix,unit_matrix

def third_operation(real_matrix,unit_matrix): # makes zero the upper triangle
    for yi in range(len(real_matrix) - 1,0,-1):
        first_number = real_matrix[yi][yi]
        for ki in range(yi):
            multiplying_element = round(-(real_matrix[ki][yi] /first_number), 2)
            real_matrix[ki] = add_onelist_scalarmultiple_theanother(real_matrix[yi], real_matrix[ki], multiplying_element)
            unit_matrix[ki] = add_onelist_scalarmultiple_theanother(unit_matrix[yi], unit_matrix[ki], multiplying_element)
    return real_matrix, unit_matrix

def main():
    try:
        # sys.argv[0] will be the file itself
        aim_of_the_code = sys.argv[1]  # enc/dec
        key_file_path = sys.argv[2]
        input_file_path = sys.argv[3]
        output_name = sys.argv[4]
        size_of_the_key_matrix = take_key_matrix(key_file_path)[1]
        key_matrix = take_key_matrix(key_file_path)[0]
        for line in key_matrix:
            assert line!=[0]*size_of_the_key_matrix , "Your key matrix does not have inverse."
        assert aim_of_the_code in ("enc", "dec") ,"Undefined parameter error: you should enter only 'enc' or only 'dec' for operation type."
        #For the following two, not using assert statement seemed more convenient to me
        if filenotfoundforkey(key_file_path) in ("Key file not found.","Key file could not be read due to unicode error.","Key file could not be read due to permission error."):
            raise IOError(filenotfoundforkey(key_file_path))
        if Filenotfoundforinput(input_file_path) in ("Input file not found.","The input file could not be read due to unicode error.","The input file could not be read due to permission error."):
            raise IOError(Filenotfoundforinput(input_file_path))

        if aim_of_the_code == "enc":
            message_matrix = convert_plain_input_to_matrix(input_file_path, translate_dictionary(),
                                                          size_of_the_key_matrix)
            new_message_matrix = operabilitiy(message_matrix)
            multiplied_one = multiply_key_with_input(key_matrix, new_message_matrix)
            write_for_enc(output_name, multiplied_one)
        elif aim_of_the_code == "dec":
            first_step_for_inversed=first_operation(key_matrix,unit_matrix(len(key_matrix)))
            second_step_for_inversed=second_operation(*first_step_for_inversed)
            inversed_matrix=third_operation(*second_step_for_inversed)[1]
            decoded_matrix = convert_ciphertext_to_matrix(input_file_path, size_of_the_key_matrix)
            new_message1 = operabilitiy(decoded_matrix)
            multiplied_matrix = multiply_key_with_input(inversed_matrix, new_message1)
            text = matrix_to_text_for_dec(multiplied_matrix)
            write_for_dec(output_name, text)

    except IndexError : #for command line argument number
        print("You should enter 4 parameters besides of your file name (operation type, key file path,input file path, output file name)")
        sys.exit()
    except FileNotFoundError as e:
        print(e)
        sys.exit()
    except IOError as e:
        print(e)
        sys.exit()
    except AssertionError as e:
        print(e)
        sys.exit()
    except Exception:
        print("kaBOOM: run for your life!")
        sys.exit()

if __name__=="__main__":
    main()