#1 ex
import re

pattern = r"ab*"
text = "abbb abb a ac abc"
matches = re.findall(pattern, text)
print(matches)

#2 ex
pattern = r"ab{2,3}"
text = "ab aab abbb abbbb abbbbb"
matches = re.findall(pattern, text)
print(matches) 

#3 ex
pattern = r"[a-z]+_[a-z]+"
text = "hello_world test_case snake_case Upper_Case"
matches = re.findall(pattern, text)
print(matches) 

#4 ex
pattern = r"[A-Z][a-z]+"
text = "Hello World TEST Aword NextStep"
matches = re.findall(pattern, text)
print(matches) 

#5 ex
pattern = r"a.*b"
text = "acb a123b axxxb ab a_b"
matches = re.findall(pattern, text)
print(matches)  # ['acb', 'a123b', 'axxxb', 'ab', 'a_b']

#6
pattern = r"[ ,.]"
text = "Hello, world. How are you"
result = re.sub(pattern, ":", text)
print(result)  # Hello::world::How:are:you
