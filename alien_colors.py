alien_color = "green"

if alien_color == "green":
    print("You earn 5 points!")

alien_color = "red"

if alien_color != "green":
    print("You lose...")

alien_color = "cyan"

if alien_color == "green":
    print("You have earned 5 points")
elif alien_color == "yellow":
    print("Your score is 3")
elif alien_color == "red":
    print("You lose...")
else:
    print("Wrong Color!!!\n\n") 

age = 13

if age < 2:
    print("You are a baby...")
elif (age == 2) or (age < 4):
    print("you are a toddler...")
elif (age == 4) or (age < 13):
    print("You are a kid...")
elif (age == 13) or (age < 20):
    print("You are a teenager...")
elif (age == 20) or (age < 65):
    print("You are adult...")
elif age >= 65:
    print("You are an elder...")


favorite_fruits = ['banana', 'apple', 'orange']

fruit = 'apricot'

if fruit not in favorite_fruits:
    print("You really like", fruit.title())

