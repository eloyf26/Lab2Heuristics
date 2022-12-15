from queue import PriorityQueue

class Student():
    def  __init__(self,id ="-1",trouble = False,reduced = False ,seat = -1,empty = False, valid = True,cost = 1):
        self.id = id
        self.trouble = trouble
        self.reduced = reduced
        self.seat = seat
        self.empty = empty
        self.valid = valid
        self.cost = cost

def PathCost(state):
    cost = 0
    reduced = False
    prevcost= 0
    trouble = []
    count = 0
    for student in state.path:
        tempcost = 0
        #Case where prev student is normal so we only calculate the cost of the student
        if reduced == False:
            if student.reduced == True:
                tempcost +=  3
                reduced = True
            else:
                tempcost += 1

            if student.trouble == True:
                trouble.append(student.seat) 

            #not firstudent
            if count != 0:
                if state.path[count-1].trouble == True:
                    tempcost *= 2
            #not laststudent
            if count != len(state.path) - 1: 
                if state.path[count+1].trouble == True:
                    tempcost *= 2

            for t in trouble:
                if t < student.seat:
                    tempcost *= 2


        #if prev Student is reduced(then next has to be normal so the cost of the student is the same as the reduced)
        elif reduced == True:
            reduced = False

        cost += tempcost
        count += 1

    return cost

def PathCost2(state):
    cost = 0
    reduced = False
    prevcost= 0
    trouble = []
    count = 0
    for student in state.path:
        tempcost = 0
        #Case where prev student is normal so we only calculate the cost of the student
        if reduced == False:
            if student.reduced == True:
                tempcost +=  3
                reduced = True
            else:
                tempcost += 1

            if student.trouble == True:
                trouble.append(student.seat) 

            #not firstudent
            if count != 0:
                if state.path[count-1].trouble == True:
                    tempcost *= 2
            #not laststudent
            if count != len(state.path) - 1: 
                if state.path[count+1].trouble == True:
                    tempcost *= 2

            for t in trouble:
                if t < student.seat:
                    tempcost *= 2


        #if prev Student is reduced(then next has to be normal so the cost of the student is the same as the reduced)
        elif reduced == True:
            reduced = False
        print (tempcost)
        cost += tempcost
        count += 1

    return cost

class State_Bus_Distribution():
    def __init__(self, parent, value, missingList, start, goal):


        self.children = []
        self.parent = parent
        self.value = value
        self.heuristicCost = 0
        self.valid = True

        copyList = missingList[:]
        if self.value not in copyList:
            self.missingList = copyList
        else:
            copyList.remove(self.value)
            self.missingList = copyList

        
        if parent:
            self.path = parent.path[:]
            self.AddStudent()
            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = []
            self.start = start
            self.goal = goal

        self.heuristicCost = self.GetHeuristicCost1()
         
    def CreateChildren(self):
        for missingStudent in self.missingList: 
            children = State_Bus_Distribution(self,missingStudent,self.missingList,self.start, self.goal)
            self.children.append(children)
                 
    def GetHeuristicCost2(self):
        heuristicCost = 0
        for student in self.missingList:
            if student.reduced:
                heuristicCost += 3
            else:
                heuristicCost += 1
                
        return heuristicCost

    def GetHeuristicCost1(self):
        return len(self.missingList)
            
    def AddStudent(self):
        #Make sure that path is not empty
        if len(self.path) == 0:
            self.path.append(self.value)
            return
        elif (len(self.missingList)==0) and self.value.reduced:
            print("Reduced movility last is not allowed")
            self.valid = False
        elif self.value.reduced and self.path[-1].reduced:
            print("two reduced not allowed") 
            self.valid = False

        self.path.append(self.value)
        return


class AstarSolver:
    def __init__(self,students, start, goal):
        self.path = []
        self.visitedQueu = []
        self.priorityQueu = PriorityQueue()
        self.start = start 
        self.goal = goal
        self.studentList = students
        self.cost = 0

    def Solve(self):
        startState = State_Bus_Distribution(0, self.start, self.studentList, self.start, self.goal)
        count = 0
        self.priorityQueu.put((0,count,startState))
        #While not having path and priorityqueu size not empty
        while (not self.path and self.priorityQueu.qsize()):
            state_touple = self.priorityQueu.get()
            closestChild = state_touple[2]
            if count != 0:
                print ("Expanded student: " + str(closestChild.value.id) + " Expanded STATE: " + str(state_touple[1]))
                for i in closestChild.path:
                    print (i.id)
            print(str(self.priorityQueu.qsize()) + " start")
            closestChild.CreateChildren()
            self.visitedQueu.append(closestChild)
            for child in closestChild.children:
                if child.valid:
                    print ("Checking child: " + str(child.value.id))
                    if child not in self.visitedQueu:
                        count += 1
                        self.cost = child.heuristicCost + PathCost(child)
                        print(str(len(child.missingList)) + " Missing list")
                        print(str(child.heuristicCost) + " Heuristic cost" )
                        print(str(self.cost) + " child TOTAL COST" )
                        if not child.heuristicCost:
                            self.path = child.path
                            break
                        self.priorityQueu.put((self.cost, count, child))
            print(str(self.priorityQueu.qsize()) + " end")
        if not self.path:
            print ("This student combination is not possible")
            return
        return self

#Functions to read the input file in appropiate format
def obtainseats(seatsarray):
    if len(seatsarray) == 3:
        seat = int(seatsarray[1] + seatsarray[2])
    elif len(seatsarray) == 2:
        seat = int(seatsarray[1])
    else:
        raise Exception("Not correct seat format")

    return seat


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
    
        student = Student(id,trouble,reduced,seat,empty=False,valid=True)
        students.append(student)

    initQtxt.close()
    #print(students)
    
    return students

if __name__ == "__main__":

    students = ReadInputFile(r"C:\Users\eloyfernandez\Documents\Uni\Heuristica\Lab2\Lab2Heuristics\prueba6.txt")

    start = []
    goal = students[:]

    solver = AstarSolver(students,start,goal)
    solution = solver.Solve()
    if solution:    
        print ("\nTotal cost of the path is: " + str(solution.cost))
        print ("\nThe ordered list of students is: ")
        for child in solution.path:
            print ("ID: " + str(child.id) + "\t" + "Student cost: " + str(child.cost) + "\t" + " Student seat: " + str(child.seat))