from constraint import *

def main():

    #Setting up initial variables
    rows = 4
    columns = 8 

    problem = Problem()
    problem.addVariables(columns,rows)

    reduced_movility = [1,2,3,4,13,14,15,16,17,18,19,20]
    section1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    section2 = [17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]

def ReadInputFile():
    
    #Input file follow this format: (1/2/.../n),(1/2),(C/X),(R/X),(Sibling ID, 0 if non)
    # For example: 1,1,C,X,3 . Student ID:1 , Year:1 , Troublesome: C(Troublesome), Mobility: X(Not Reduced), SiblingId: 3  
    
    pathToJson
    f = open()