from constraint import *
import numpy as np

#Function to obtain the Students from the input file

def ReadInputFile():

    studentsTxt = open('Students.txt','r')
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
    siblingIds = [] 
    for pair in siblingPairs:
        siblingIds.append(pair[0])
        siblingIds.append(pair[1])

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

    firstYearStudentIds,secondYearStudentIds,realSecond = moveSiblingsToSameSection(siblingPairs,firstYearStudentIds,secondYearStudentIds)

    redMobFirstYearIds = intersection(redMobStudentIds,firstYearStudentIds)
    redMobSecondYearIds = intersection(redMobStudentIds,secondYearStudentIds)

    #Defining Constraints:

    #1 per seat
    problem.addConstraint(AllDifferentConstraint(),[id for id in studentIds])
    #Reduced Mobility seats
    for id in redMobFirstYearIds:
        problem.addConstraint(lambda a: a in redMobSection1, id)
    for id in redMobSecondYearIds:
        problem.addConstraint(lambda a: a in redMobSection2, id)   
    #Not next to reduced mobility
    for id1 in redMobFirstYearIds + redMobSecondYearIds:
        for id2 in studentIds:
            problem.addConstraint(NotNextToSeatCondition, (id1,id2))
    #First year seats
    for id in firstYearStudentIds:
        problem.addConstraint(lambda a: a in section1, id)
    #Second year seats
    for id in secondYearStudentIds:
        problem.addConstraint(lambda a: a in section2, id)
    #Not adjacent to troublesome
    for id1 in troubleStudentIds:
        for id2 in troubleStudentIds + redMobStudentIds:
            if id1 != id2:
                problem.addConstraint(NotAdjacentSeatCondition,(id1,id2))
    solution = problem.getSolution()
    print(solution)
    #Silbling next to each other
    for pair in siblingPairs:
        for id in realSecond:
            if pair[0] == id:
                problem.addConstraint(NotSameYearCondition,(pair[1],pair[0]))
            elif pair[1] == id:
                problem.addConstraint(NotSameYearCondition,(pair[0],pair[1]))
            else:
                problem.addConstraint(lambda a,b: not(NotNextToSeatCondition),(pair[0],pair[1],True))
    solution = problem.getSolution()
    print(solution)

def NotSameYearCondition(youngSibling, oldSibling):
    return SiblingsNextToEachOther(youngSibling, oldSibling, False)

def SiblingsNextToEachOther(youngSibling, oldSibling, sameYear):   
    if (not sameYear):
        if ((oldSibling % 2 == 0) and (oldSibling - youngSibling == 1)):
            return True
        elif ((oldSibling % 2 == 1) and (oldSibling - youngSibling == -1)):
            return True
    else:
        return not(NotNextToSeatCondition(oldSibling,youngSibling))

def moveSiblingsToSameSection(siblingPairs,firstYearStudentIds,secondYearStudentIds):
    realSecond =[]
    for pair in siblingPairs:
        if pair[0] in firstYearStudentIds and pair[1] in secondYearStudentIds:
            firstYearStudentIds.append(pair[1])
            realSecond.append(pair[1])
            secondYearStudentIds.remove(pair[1])
        elif pair[1] in firstYearStudentIds and pair[0] in secondYearStudentIds:
            firstYearStudentIds.append(pair[0])
            realSecond.append(pair[0])
            secondYearStudentIds.remove(pair[0])

    return firstYearStudentIds,secondYearStudentIds,realSecond

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
    totalMatrix = np.matrix([[29,25,21,17,13,9,5,1],[30,26,22,18,14,10,6,2],[31,27,23,19,15,11,7,3],[32,28,24,20,16,12,8,4]])
    if (b in adj_finder(totalMatrix,a)):
        return False
    return True

def adj_finder(matrix, element):
    position = np.where(matrix == element)
    mat = np.asarray(matrix)
    a, b = (position[0][0], position[1][0]) # the index of the element 
    adj = [mat[i][j] for i in range(a-1, a+2) for j in range(b-1, b+2) if i > -1 and j > -1 and j < len(mat[0]) and i < len(mat)]
    adj.remove(element)
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
