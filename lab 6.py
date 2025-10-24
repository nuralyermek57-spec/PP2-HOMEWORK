# 1 ex
# def function(multiplication):
#     result = 1
#     for i in multiplication:
#         result *= i
#     return result

# example_list = [2, 3, 4, 5]
# print(function(example_list))

# 2 ex
# def case_counter(string):
#     upper = 0
#     lower = 0
#     for i in string:
#         if i >= 'A' and i <= 'Z':
#             upper += 1
#         elif i >= 'a' and i <= 'z':
#             lower += 1
#     return upper, lower

# example_word = "Hello World"
# u, l = case_counter(example_word)
# print("Uppercase number:", u)
# print("Lowercase number:", l)

# 3 ex
#  def palindrome_checker(s):
#     s = s.lower().replace(" ", "")
#     return s == s[::-1]

# word = "Madam"
# print("Is the word palindrome?", palindrome_checker(word))

# 5 ex
# def true_checker(tup):
#     return all(tup)

# example_tuple = (1, "hello", 2.5431)
# print(true_checker(example_tuple))

# 1 ex

import os

# address = "repository" 

# print("Directories:")
# for folder in os.listdir(address):
#     if os.path.isdir(os.path.join(address, folder)):
#         print( folder)

# print("Files:")
# for file in os.listdir(address):
#     if os.path.isfile(os.path.join(address, file)):
#         print(file)

# 3 ex
# path = "example"

# if os.path.exists(path):
#     print("Path exists.")
#     print("Filename:", os.path.basename(path))
#     print("Directory:", os.path.dirname(path))
# else:
#     print("Path does not exist.")

import os

path = "test.txt"

print("Exists?", os.access(path, os.F_OK))   
print("Readable?", os.access(path, os.R_OK)) 
print("Writable?", os.access(path, os.W_OK)) 
print("Executable?", os.access(path, os.X_OK)) 

