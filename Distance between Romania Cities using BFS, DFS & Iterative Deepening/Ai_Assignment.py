import os

parentChild={}
pathList=[]

class Node:
    def __init__(self,name,parent,children,pathCost):
        self.name=name
        self.parent=parent
        self.children=children
        self.pathCost=pathCost
        self.visited=False



def readInputFile():
    path=os.getcwd()+'\Resources\RomaniaPath.csv'
    filePointer=open(path,'r')
    for values in filePointer:
        row=values.split(',')
        #childCost.update({row[1]:row[2]})
        childCost={}
        childCost[row[1].lower()]=row[2]
        if(parentChild.has_key(row[0].lower())==False):
            parentChild[row[0].lower()]=[childCost]
        else:
            parentChild[row[0].lower()].append(childCost)
        childCost={}
        childCost[row[0].lower()]=row[2]
        if(parentChild.has_key(row[1].lower())==False):
            parentChild[row[1].lower()]=[childCost]
        else:
            parentChild[row[1].lower()].append(childCost)

#dfsRecurDistance=0

def DFSRecursive(source):
    root=Node(source,None,parentChild.get(source),0)
    return findPathRecurDFS(root)

#dfsRecurDistance=0
exploredDFS=[]
def findPathRecurDFS(source):
    source.visited=True
    exploredDFS.append(source.name)
    count=0
    for child in parentChild.get(source.name):
        length=len(parentChild[source.name])
        if  child.keys()[0] not in exploredDFS :
            node=Node(child.keys()[0],source,parentChild.get(child.keys()[0]),child.get(child.keys()[0]))
            if child.keys()[0] in destination:
                pathList.append(str(node.name).title())
                pathList.append(str(source.name).title())
                #print node.name," - ",source.name,
                return int(node.pathCost)
            returneValue=findPathRecurDFS(node)
            if returneValue:
                pathList.append(str(source.name).title())
                #print " - ",source.name,
                return int(returneValue)+int(node.pathCost)
        else:
            count+=1
            if count==length:
                return False


exploredIterative=[]
def IterativeDeepninng(source):
    if source in destination:
            print "Source node is the destination node"
            return 0
    root=Node(source,None,parentChild.get(source),0)
    """
    element=exploredIterative.pop()
    while element:
        element=exploredIterative.pop()
    """
    for limit in range(1,19):
        length=len(exploredIterative)
        for i in range(0,length):
            exploredIterative.pop()
        returnValue=findIterativeDeepninng(root,limit)
        if returnValue:
            return returnValue



def findIterativeDeepninng(source,limit):

    if limit==0:
        return False
    source.visited=True
    exploredIterative.append(source.name)
    count=0
    for child in parentChild.get(source.name):
        length=len(parentChild[source.name])
        if  child.keys()[0] not in exploredIterative :
            count+=1
            node=Node(child.keys()[0],source,parentChild.get(child.keys()[0]),child.get(child.keys()[0]))
            if child.keys()[0] in destination:
                pathList.append(str(node.name).title())
                pathList.append(str(source.name).title())
                #print node.name," - ",source.name,
                return int(node.pathCost)
            returneValue=findIterativeDeepninng(node,limit-1)
            if returneValue:
                pathList.append(str(source.name).title())
                #print " - ",source.name,
                return int(returneValue)+int(node.pathCost)
            else:
                node.visited=False
                if count==length:
                    exploredIterative.remove(source.name)
                    return False
        else:
            count+=1
            if count==length:
                exploredIterative.remove(source.name)
                return False


def BFS(source):
    root=Node(source,None,parentChild.get(source),0)
    return findPathBFS(root)

def findPathBFS(source):
    exploredBFS=[]
    discover=[]
    frontierName=[]
    discover.append(source)
    frontierName.append(source.name)
    source.visited=True
    if source.name in destination:
            print "Source node is the destination node"
            return 0
    while len(discover) !=0:
        fetch=discover.pop(0)
        #print(fetch.name),
        fetch.visited=True
        exploredBFS.append(fetch.name)
        for child in parentChild.get(fetch.name):
            if child.keys()[0] not in exploredBFS or child.keys()[0] not in frontierName :
                node=Node(child.keys()[0],fetch,parentChild.get(child.keys()[0]),child.get(child.keys()[0]))
                #print(node.name),
                if child.keys()[0] in destination:
                    distance=0
                    print "\nHere is the path:"
                    while node.parent:
                        distance+= int(node.pathCost)
                        pathList.append(str(node.name).title())
                        #print str(node.name).title()+" -",
                        node=node.parent
                    pathList.append(str(source.name).title())
                    #print(str(source.name).title()+" = "),
                    return distance
                discover.append(node)
                frontierName.append(node.name)

readInputFile()

loop=True
while(loop):

    while(loop):
        source=raw_input('\nEnter a source: ')
        source=source.lower()
        if parentChild.get(source):
            loop=False
        else:
            print "Please enter a valid City name"


    loop=True
    while(loop):
        destination=raw_input('\nEnter a destination: ')
        destination=destination.lower()
        if parentChild.get(destination):
            loop=False
        else:
            print "Please enter a valid City name"


    loop=True
    searchType = raw_input("\nWhich Search you want to perform \n 1 BFS \n 2 DFS \n 3 Iterative Deepening\n 4 Exit")
    if searchType=="1":
        pathCost= BFS(source)
        for i in range(0,len(pathList)):
            print pathList[len(pathList)-i-1]," - ",
        print pathCost
        exploredBFS=[]
        pathList=[]
    elif searchType=="2":
        pathCost=DFSRecursive(source)
        for i in range(0,len(pathList)):
            print pathList[len(pathList)-i-1]," - ",
        print pathCost
        exploredDFS=[]
        pathList=[]
    elif searchType=="3":
        pathCost= IterativeDeepninng(source)
        for i in range(0,len(pathList)):
            print pathList[len(pathList)-i-1]," - ",
        print pathCost
        exploredIterative=[]
        pathList=[]
    elif searchType=="4":
        loop=False
    else:
        print "Invalid Input"

    cont= str(raw_input("\nDo you want to continue\nY\nN\n")).lower()
    if cont=="n":
        loop=False


