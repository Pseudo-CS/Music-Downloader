import math as m
C = 50
H = 30
l2 = input("Enter data that needs to be found ")
D = l2.split(",")
Q=[]
  
for i in D:
    F =  (2 * C * int(i))/H
    Q.append(str(m.sqrt(F)))
print (Q)