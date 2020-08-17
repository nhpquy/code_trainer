import random

name_list = []
with open("name_list.txt", "r") as f:
    for line in f:
        if line != "":
            name_list.append(line.replace(" ", "").replace("\n", ""))
f.close()
#
fw = open("out.txt", "w")
for i in range(0, 100):
    new_email = random.choice(name_list) + str(random.randint(0, 100000)) + "@gmail.com\n"
    fw.write(new_email)

fw.close()
