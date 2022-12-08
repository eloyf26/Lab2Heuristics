from queue import PriorityQueue
import sys

#Functions to read the input file in appropiate format
def ReadInputFile(input):

    students  = []
    initQtxt = open(input,'r')

    s = initQtxt.read().split(",")
    for s in s:
        s = s.strip('{').strip('}')
        s2 = s.split(":")
        s2[0] = s2[0].lstrip()
        seat = obtainseats(s2[1])
        #double digit id
        if len(s2[0]) == 4:
            id = s2[0][0] + s2[0][1]
            if s2[0][2] == 'C':
                trouble = True
            else:
                trouble  = False
            if s2[0][3] == 'R':
                reduced = True
            else:
                reduced = False
        #single digit id   
        else:
            id = s2[0][0]
            if s2[0][1] == 'C':
                trouble = True
            else:
                trouble  = False
            if s2[0][2] == 'R':
                reduced = True
            else:
                reduced = False
        student = Student(id,trouble,reduced,seat,empty=False)
        students.append(student)

    initQtxt.close()
    #print(students)
    
    return students

def obtainseats(seatsarray):
    if len(seatsarray) == 3:
        seat = int(seatsarray[1] + seatsarray[2])
    elif len(seatsarray) == 2:
        seat = int(seatsarray[1])
    else:
        raise Exception("Not correct seat format")

    return seat

class Node:
    def __init__(self,state,pool,heuristic):

        self.state = state
        self.pool = pool
        if heuristic == 1:
            self.heuristic = Heuristic1(state)
        if heuristic == 2:
            self.heuristic = Heuristic2(state)
        self.neighbours = neighbours(state,pool,heuristic)

    def __lt__(self, other):
        return True

class Student():
    def  __init__(self,id ="-1",trouble = False,reduced = False ,seat = -1,empty = False):
        self.id = id
        self.trouble = trouble
        self.reduced = reduced
        self.seat = seat
        self.empty = empty


#Astar Function

def Astar(initial):
    queue = PriorityQueue()
    queue.put(initial,0)
    cost_so_far = {initial: 0}
    #cost_so_far = 0
    solution = []
    while not queue.empty():
        current = queue.get()

        if FinalState(current):
            return

        for next in current.neighbours:
            new_cost = cost_so_far[current] + 1
            #new_cost = cost_so_far + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                fn = new_cost + current.heuristic
                print(current.heuristic)
                queue.put(next,fn)

    return cost_so_far

#Function to obtain the next possibilities of students on the Queue
def neighbours(state,pool,heuristic):
    options = []
    count = 0
    for s in state:
        if s.empty == True:
            break
        else:
            count += 1

    for p in pool:
        #print(len(state))
        #print(count)
        state[count-1] = p
        if CheckState(state):
            newpool = []
            for x in pool:
                if x != p:
                    newpool.append(x)

            node = Node(state,newpool,heuristic)
            options.append(node)

    return options


#Heuristic one , where we relax the troublesome constraints
def Heuristic1(state):

    cost = 0   
    reduced = False  
    for student in state:

        if student.empty == True:
            return cost 

        #Case where prev student is normal so we only calculate the cost of the student    
        if reduced == False:
            if student.reduced == True:
                cost = cost + 3
            else:
                cost = cost + 1

        #if prev Student is reduced(then next has to be normal so the cost of the student is the same as the reduced)
        if reduced == True:
            cost = cost + 3
        
    return cost

    #Cost of Reduced = x3 Not reduced  = x1
    #Behind Reduced goes with him

#Heuristic two, where we relax the reduced movility 
def Heuristic2(state):

    cost  = 0

    return cost

    #Troule = x2 behind and ahead
    #Trouble Double time of students behind queue and higher seat number


#Function to obtain the time of a solution
def Checktime (solution):
    time = 0
    return time


#Checks if a state is posible
def CheckState(state):
    #state = Node.state
    #No last reduced movility
    if state[-1].reduced == True:
        return False

    #Not 2 consecutive Reduced Movility
    reduced = False
    for student in state:
        if student.reduced == True and reduced == True:
            return False
        reduced  = student.reduced

    
    return True

#Checks if a state is a final state
def FinalState(Node):

    for student in Node.state:
        if student.empty == True:
            return False

    return True


#Functions to Produce the 2 output files
def solution(pathfile,initial,final):

    #pathToOutput = pathfile[0:-3] + "output"
    outputFile = open("output.txt",'w')
    outputFile.write("Initial: ")
    outputFile.write("{")
    last = initial[-1]
    for student in initial:
        outputFile.write("'")
        outputFile.write(student.id)
        if student.reduced == False:
            outputFile.write("X")
        else:
            outputFile.write("R")
        if student.trouble == False:
            outputFile.write("X")
        else:
            outputFile.write("C")
        outputFile.write("': ")
        outputFile.write(str(student.seat))
        if student != last:
            outputFile.write(", ")
    outputFile.write("}")
    outputFile.write("\n")


    outputFile.write("Final: ")
    outputFile.write("{")
    last = final[-1]
    for student in final:
        outputFile.write("'")
        outputFile.write(student.id)
        if student.reduced == False:
            outputFile.write("X")
        else:
            outputFile.write("R")
        if student.trouble == False:
            outputFile.write("X")
        else:
            outputFile.write("C")
        outputFile.write("': ")
        outputFile.write(str(student.seat))
        if student != last:
            outputFile.write(", ")
    outputFile.write("}")
    
    return

def statistics(pathfile,time,cost,length):

    outputFile = open(pathfile ,'w')
    outputFile.write("Total time: "+ time + "\n")
    outputFile.write("Total cost: "+ time + "\n")
    outputFile.write("Plan length: "+ time + "\n")
    outputFile.write("Plan cost: "+ time + "\n")

    return


#Main Function
def main(students,heuristic):

    # Read the file
    students  = ReadInputFile(students) #pool of students
    
    lenQ = len(students) 
    empty = Student(empty=True)
    # Initialize the start State which is queue of empty students
    initState = [empty] * lenQ

    initialnode = Node (initState,students,heuristic)
    cost = Astar(initialnode)
    solution(students,students,students)
    return

if __name__ == '__main__':
    
    #pathstudents = sys.argv[1]
    #heuristic = sys.argv[2]
    pathstudents = "prueba.txt"
    heuristic = 1
    main(pathstudents,heuristic)

    