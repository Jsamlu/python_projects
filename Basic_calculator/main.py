
def Calculator(num1, num2, opr):
    opr_check = {
        '+' : num1+num2,
        '-' : num1-num2,
        '*' : num1*num2,
        '/' : num1/num2,
    }
    return opr_check.get(opr, "nothing")

print("Enter two values\n")
num1= int(input("Enter the first value:\n"))
num2 = int(input("Enter the second value\n"))
Opr = input("Ente the Opreation:\n")

print(Calculator(num1, num2, Opr))



