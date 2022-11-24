
import sys

def Heuristic1():
    return

def Heuristic2():
    return

#Functions to read the input file in appropiate format
def ReadInputFile(input):

    students  = []
    initQtxt = open("prueba.txt",'r')

    s = initQtxt.read().split(",")
    for s in s:
        s = s.strip('{').strip('}')
        s2 = s.split(":")
        s2[0] = s2[0].lstrip()
        s2[1] = obtainseats(s2[1])
        students.append(s2)
    
    initQtxt.close()
    
    print(students)
    
    return students

def obtainseats(seatsarray):
    if len(seatsarray) == 3:
        seat = int(seatsarray[1] + seatsarray[2])
    elif len(seatsarray) == 2:
        seat = int(seatsarray[1])
    else:
        raise Exception("Not correct seat format")

    return seat


#Functions to Produce the 2 output files
def solution():

    print("INITIAL")
    print("FINAL")

    return

def statistics():


    print("Total time:")
    print("Total cost:")
    print("Plan length:")
    print("Plan cost:")

    return

#Main Function
def main(initQ):

    #Cost of Reduced = x3 Not reduced  = x1
    #Not 2 consecutive Reduced Movility
    #Behind Reduced goes with him
    #Troule = x2 behind and ahead
    #Trouble Double time of students behind queue and higher seat number

    #No last reduced movility

    lenQ = len(initQ)
    initState = [0] * lenQ
    
    
    return

if __name__ == '__main__':
    
    students = sys.argv[1]
    heuristic = sys.argv[2]

    initQ = ReadInputFile(students)
    main(initQ)
    
