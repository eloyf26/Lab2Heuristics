from constraint import *
import numpy as np

#Function to obtain the Students from the input file

def ReadInputFile():

    studentsTxt = open('Students2.txt','r')
    students = []
    for line in studentsTxt.read().splitlines():
        s = line.split(",")
        students.append(s)

    studentsTxt.close()

    return students



def main():

    students = ReadInputFile()

    #Setting up initial variables
    numSeats = 32
    seats = range(1,numSeats + 1)
    
  
    problem = Problem()
    for student in students:
        problem.addVariables(student[0],seats)

    reducedMobility = [1,2,3,4,13,14,15,16,17,18,19,20]
    section1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    section2 = [17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    redMobSection1 = intersection(reducedMobility,section1)
    redMobSection2 = intersection(reducedMobility,section2)


    #We divide the domain in different sets so that we can work easier with different type of students
    studentIds = []
    redMobStudentIds = []
    firstYearStudentIds = []
    secondYearStudentIds = []
    troubleStudentIds = []
    siblingPairs = GetSiblingPairs(students)

    for student in students:
        studentIds.append(student[0])
        if (IsFirstYear(student)):
            firstYearStudentIds.append(student[0])
        else:
            secondYearStudentIds.append(student[0])

        if (IsTroublesome(student)):
            troubleStudentIds.append(student[0])

        if (IsReducedMobility(student)):
            redMobStudentIds.append(student[0])

    redMobFirstYearIds = intersection(redMobStudentIds,firstYearStudentIds)
    redMobSecondYearIds = intersection(redMobStudentIds,secondYearStudentIds)

    #Defining Constraints:

    #1 per seat
    problem.addConstraint(AllDifferentConstraint(),[id for id in studentIds])
    #Reduced Mobility seats
    problem.addConstraint(CheckIfOnGroup, ([id for id in redMobFirstYearIds],redMobSection1))
    problem.addConstraint(CheckIfOnGroup, ([id for id in redMobSecondYearIds],redMobSection2))
    #problem.addConstraint(lambda a: a in redMobSection2 == True, [id for id in redMobSecondYearIds])
    solutions = problem.getSolutions()
    #Not next to reduced mobility
    problem.addConstraint(NotNextToSeatCondition, ([id1 for id1 in redMobStudentIds],[id2 for id2 in studentIds]))
    #First year seats
    problem.addConstraint(lambda a: a in section1 == True, [id for student[0] in firstYearStudentIds])
    #Second year seats
    problem.addConstraint(lambda a: a in section2 == True, [id for student[0] in secondYearStudentIds])
    #Not adjacent to troublesome
    problem.addConstraint(NotAdjacentSeatCondition, ([id1 for id1 in troubleStudentIds],[id2 for id2 in studentIds]))
    #Silbling in same section


def CheckIfOnGroup(a,group):
    return (a in group)

def GetSiblingPairs(students):
    siblings = []
    for student in students:
        #IF student has siblings
        if (student[4]!= '0'): 
            #If not already on list
            #Check if the sibling was already added (and thus, himself too)
            if ([student[4],student[0]] not in siblings):   
                siblings.append([student[0],student[4]])    
    
    return siblings

def NotNextToSeatCondition(a,b):
    #Odd and even numbers have different adjacent seats (not symmetric)
    if ((a % 2 == 0) and (a - b == 1)):
        return False
    elif ((a % 2 == 1) and (a - b == -1)):
        return False
    return True

def NotAdjacentSeatCondition(a,b):
    #Divide into section 1 and 2
    matrixSection1 = np.matrix([[13,9,5,1],[14,10,6,2],[15,11,7,3],[16,12,8,4]])
    matrixSection2 = np.matrix([[29,25,21,17],[30,26,22,18],[31,27,23,19],[32,28,24,20]])

    if (a in range(1,17)):
        #Check A is not adjacent to B
        if (b in adj_finder(matrixSection1,a)):
            return False
    else:
        if (b in adj_finder(matrixSection2,a)):
            return False
    return True

def adj_finder(matrix, element):
    position = matrix.where(element)
    adj = []
    
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            rangeX = range(0, matrix.shape[0])  # X bounds
            rangeY = range(0, matrix.shape[1])  # Y bounds
            
            (newX, newY) = (position[0]+dx, position[1]+dy)  # adjacent cell
            
            if (newX in rangeX) and (newY in rangeY) and (dx, dy) != (0, 0):
                adj.append((newX, newY))
    
    return adj

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3    

#Return certain 'characteristic' based on studentId 
def studentCharacteristic(characteristic, studentId, students):
    # characteristic: StudentID = 0, year = 1, troublesome = 2, Mobility = 3, siblings = 4
    for student in students:
        if (studentId == student[0]):
            if (characteristic in range(0,5)):
                return student[characteristic]
            else:
                raise Exception("characteristic not in range 0 to 4")
        else:
            raise Exception("studentId not found in list of students")

def IsReducedMobility(student):
    Mobility = student[3]
    if (Mobility == "R"):
        return True
    elif (Mobility == "X"):
        return False
    else:
        raise Exception("Mobility format is not valid")

def IsTroublesome(student):
    trouble = student[2]
    if (trouble == "C"):
        return True
    elif (trouble == "X"):
        return False
    else:
        raise Exception("Trouble format is not valid")

def IsFirstYear(student):
    year = student[1]
    if (year == "1"):
        return True
    elif (year == "2"):
        return False
    else:
        raise Exception("Year format is not valid")



main()
