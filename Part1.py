import constraint import *

#Class to Represents Students

class Student:
    def __init__(self,Id,Year,Trouble,Mobility,IdSibling):
        self.Id = Id
        self.Year = Year
        self.Trouble = Trouble
        self.Mobility = Mobility
        self.IdSibling = IdSibling


#Function to obtain the Students from the input file

def ReadInputFile():

    students = open('Students.txt','r')
    while(True):
        line = students.readline()

        if not line:
            break

        line.split(',')

        Id = line[0]
        Year = line[1]
        Trouble = line[2]
        Mobility = line[3]
        Idsibling = line[4]

        s = Student(Id,Year,Trouble,Mobility,Idsibling)

    students.close()



def main():

    #Setting up initial variables
    rows = 4
    columns = 8 

    problem = Problem()
    problem.addVariables(columns,rows)

    reduced_movility = [1,2,3,4,13,14,15,16,17,18,19,20]
    section1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    section2 = [17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]



    #Defining Constraints

if __name__ == '__main__':
