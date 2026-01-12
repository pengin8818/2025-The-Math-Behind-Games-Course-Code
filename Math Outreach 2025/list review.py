demo_list = ["apple", "grape", "blueberry", "orange"]

other_list = ["red", "green", "blue", "orange"]

for index in range(len(other_list)):
    print(other_list[index], demo_list[index])


demo_list.append(5)

print(demo_list)