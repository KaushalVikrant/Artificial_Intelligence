import numpy as np
import sys


totalRandomProbability=50000
#numberOfSamples=100000
randomList=np.random.uniform(0, 1,totalRandomProbability)
parentsDict={}
finalList=[]
finalAdditionList=[]
topologicalOrder=["B","E","A","J","M"]

class Node:
    def __init__(self,name,parent,children,variables,value):
        self.name=name
        self.parent=parent
        self.children=children
        self.variables=variables
        self.value=value


def constructCPT():
    cptDict={}
    cptDict.update({"B":{"t":.001}})
    cptDict.update({"E":{"t":.002}})
    cptDict.update({"A":{"tt":.95,"tf":.94,"ft":.29,"ff":.001}})
    cptDict.update({"J":{"t":.90,"f":.05}})
    cptDict.update({"M":{"t":.7,"f":.01}})
    return cptDict


def setParents():
    global parentsDict
    parentsDict.update({"J":["A"]})
    parentsDict.update({"M":["A"]})
    parentsDict.update({"A":["B","E"]})
    parentsDict.update({"B":None})
    parentsDict.update({"E":None})

def genSearchQuery(inputList):
    searchQueryDict={}
    for i in inputList:
        tempArr = i.split(" ")
        index = topologicalOrder.index(tempArr[0])
        searchQueryDict.update({index: tempArr[1]})
    return searchQueryDict

def isQueryPresent(queryDict,patternList):
    for i in queryDict:
        if patternList[i] != queryDict[i]:
            return False
    return True

def priorSampling(numberOfSamples):
    global topologicalOrder
    collectedSampleList=[]
    cptDict=constructCPT()
    probCount=0
    for i in range(0,numberOfSamples):
          searchQuery = ""
          sample=[]
          for node in topologicalOrder:
                #probability=randomList[probCount]
                #probCount+=1
                probability = np.random.uniform(0, 1)
                if node == "B" or node =="E":
                    searchQuery="t"
                elif node=="A":
                    searchQuery=sample[0]+sample[1]
                elif node == "J" or node=="M":
                    searchQuery=sample[2]

                if probability <= cptDict.get(node).get(searchQuery):
                        sample.append("t")
                else:
                        sample.append("f")

          collectedSampleList.append(sample)
    return collectedSampleList


#print priorSampling(numberOfSamples)
def isConsistantWithEvidance(event,evidanceQuery):
     return isQueryPresent(evidanceQuery,event)

def getDict(list):
    myDict={}
    for item in list:
        arr=item.split(" ")
        myDict.update({arr[0]:arr[1]})
    return myDict

def rejectionSampling(numberOfSamples,evidance):
    sampleList=[]
    evidanceQuery=genSearchQuery(evidance)
    for i in range(numberOfSamples):
        eventSample=priorSampling(1)
        if isConsistantWithEvidance(eventSample[0],evidanceQuery):
            sampleList.append(eventSample[0])
    return sampleList

def evalLikelyHoodWeightEvent(weightedSamples,num,deno):

    numWeightSum=0
    denoWeightSum=0
    for weightedEvent in weightedSamples:
        if isQueryPresent(num,weightedEvent):
           numWeightSum=numWeightSum+weightedEvent[5]
        if isQueryPresent(deno,weightedEvent):
            denoWeightSum=denoWeightSum+weightedEvent[5]

    return numWeightSum/denoWeightSum


def genEventForLikeliHoodWeight(noOfSamples,evidenceDict):
        eventAndWeightList=[]
        cptDict = constructCPT()
        for i in range(noOfSamples):
                sample = []
                weight = 1
                for node in topologicalOrder:
                    # probability=randomList[probCount]
                    # probCount+=1
                    probability = np.random.uniform(0, 1)
                    if node == "B" or node == "E":
                        searchQuery = "t"
                        if evidenceDict.__contains__(node):
                            tOrF=evidenceDict[node]
                            if tOrF=="t":
                              sample.append("t")
                              weight=weight*cptDict.get(node).get(searchQuery)
                            else:
                                sample.append("f")
                                weight=weight*(1-cptDict.get(node).get(searchQuery))
                            continue


                    elif node == "A":
                        searchQuery = sample[0] + sample[1]
                        if evidenceDict.__contains__(node):
                            tOrF = evidenceDict[node]
                            if tOrF == "t":
                                sample.append("t")
                                weight = weight * cptDict.get(node).get(searchQuery)
                            else:
                                sample.append("f")
                                weight = weight * (1 - cptDict.get(node).get(searchQuery))
                            continue

                    elif node == "J" or node == "M":
                        searchQuery = sample[2]
                        if evidenceDict.__contains__(node):
                            tOrF = evidenceDict[node]
                            if tOrF == "t":
                                sample.append("t")
                                weight = weight * cptDict.get(node).get(searchQuery)
                            else:
                                sample.append("f")
                                weight = weight * (1 - cptDict.get(node).get(searchQuery))
                            continue

                    if probability <= cptDict.get(node).get(searchQuery):
                        sample.append("t")
                    else:
                        sample.append("f")
                sample.append(weight)
                eventAndWeightList.append(sample)

        return eventAndWeightList

def likeliHoodWeight(numOfSamples,evidence,hypoAndEvi,isPrintBoth,isPrint=True):
    evidenceDict=getDict(evidence)
    deno=genSearchQuery(evidence)
    resultDict={}
    weightedSampleList=genEventForLikeliHoodWeight(numOfSamples,evidenceDict)
    for numerator in hypoAndEvi:
        num = genSearchQuery(numerator)
        query=numerator[-1].split(" ")
        result=evalLikelyHoodWeightEvent(weightedSampleList,num,deno)
        if isPrint:
          print query[0],result
        resultDict.update({ query[0]:result})
    if isPrintBoth :
        for numerator in hypoAndEvi:
            tempQuery=numerator[len(numerator)-1]
            arr=tempQuery.split(" ")
            numerator.remove(tempQuery)
            numerator.append(arr[0]+" f")
            num = genSearchQuery(numerator)
            print evalLikelyHoodWeightEvent(weightedSampleList, num, deno)
    return resultDict


def takeInput():
    input=raw_input()
    arr=input.split(" ")
    moreInputToCome=int(arr[0])+int(arr[1])
    inputList=[]
    while moreInputToCome>0:
        userInput=raw_input()
        inputList.append(userInput)
        moreInputToCome-=1

    hypothesis=inputList[-int(arr[1]):]
    numerator=[]
    for hypo in hypothesis:
       tempEviList=inputList[0:int(arr[0])]
       query=hypo.rstrip(" ").split(" ")
       if len(query)==2 and (query[1]=="t" or query[1]=="f"):
        tempEviList.append(hypo)
       else:
           tempEviList.append(hypo + " t")
       numerator.append(tempEviList)

    #numerator=evidance
    deno=inputList[0:int(arr[0])]
    return numerator,deno


def takeInputEnumeration():
    input=raw_input()
    arr=input.split(" ")
    moreInputToCome=int(arr[0])+int(arr[1])
    inputList=[]
    while moreInputToCome>0:
        userInput=raw_input()
        inputList.append(userInput)
        moreInputToCome-=1

    evidance=inputList[0:int(arr[0])]
    hypothesis=inputList[-int(arr[1]):]
    return hypothesis,evidance

#takeInput()
def count(sampleList,numSearchDict,denoSearchDict):
    numCount = 0
    denoCount = 0
    for sample in sampleList:
        if isQueryPresent(numSearchDict, sample):
            numCount += 1
        if isQueryPresent(denoSearchDict, sample):
            denoCount += 1
    probability = 0
    if denoCount != 0:
        probability = float(numCount) / float(denoCount)
    return probability


def enumerateAll(baseyianVariables , evidence):
    global parentsDict
    if len(baseyianVariables) == 0:
        return 1;
    first=baseyianVariables.pop()
    parents= parentsDict.get(first)
    evidencePresent=[]
    for items in evidence:
        items=items.split(" ")[0]
        evidencePresent.append(items)

    if first in evidencePresent:
        finalList.append([first,parents])
        return enumerateAll(baseyianVariables,evidence)
    else:
        finalList.append(["sum ",first,parents])
        evidenceToPass=list(evidence)
        evidenceToPass.append(first)
        return enumerateAll(baseyianVariables,evidenceToPass)

def calculateValue(hypo,hypoValue,evindence):
    cptDict=constructCPT()
    string=""
    if len(evindence)==0:
        string=hypoValue
        if string=='t':
            return cptDict.get(hypo).get('t')
        else:
            return 1-cptDict.get(hypo).get('t')
    for i in evindence:
        string+=evindence.get(i)
    if hypoValue=='t':
        return cptDict.get(hypo).get(string)
    else:
        return 1-cptDict.get(hypo).get(string)

def enumerationAsk(hypothesis, evidence, bayesianVariables):
    setParents()
    returnedList=[]
    extendedEvidence=[]
    """
    for i in evidence:
        i=i.split(" ")
        extendedEvidence.append(i[0])
    """
    global finalList
    resultDict={}
    for hypothesisVariable in hypothesis:
        tempTopologicalOrder=list(topologicalOrder)

        finalList=[]
        for x in hypothesisVariable:
            extendedEvidence=list(evidence)
            extendedEvidence.append(x)
            enumerateAll(tempTopologicalOrder , extendedEvidence)
        finalList.reverse()
        addition=[0,0]

        for i in range(0,2):
            temp="t"
            evidenceToBepassed=list(evidence)
            if i==1:
                temp="f"
            evidenceToBepassed.append(hypothesisVariable+" "+temp)
            global finalAdditionList
            finalAdditionList=[]
            calculateProbabilityUsingTree(list(finalList),evidenceToBepassed,None)

            for values in finalAdditionList:
                addition[i]+=values
        alpha=addition[0]+addition[1]
        trueValue=float(addition[0])/alpha
        falseValue=float(addition[1])/alpha
        resultDict.update({str(hypothesisVariable):trueValue})
        print str(hypothesisVariable),trueValue
        #print "False Value "+str(hypothesisVariable)+" is :"+ str(falseValue)
    return resultDict


def calculateProbabilityUsingTree(enumeratedList,evidence,parent):
    if len(enumeratedList)==0:
        finalAdditionList.append(parent.value)
        return

    #for items in enumeratedList:
    items=enumeratedList[0]

    if len(items)==2:
        variablesDict={}

        hypo=items[0]
        #hypoValue='t'
        evidenceDict=[]
        """
        if items[1]:
            for i in items[1]:
                for e in evidence:
                    e=e.split(" ")
                    if i == e[0]:
                        evidenceDict.update({i:e[1]})
        """
        findParents=parentsDict.get(items[0])
        neededEvidence={}
        if findParents:
            for p in findParents:
                if parent:
                    if p in parent.variables:
                        neededEvidence.update({p:parent.variables.get(p)})

        for e in evidence:
            e=e.split(" ")
            if items[0] == e[0]:
                hypoValue=e[1]
        """
        hypoValue='t'
        """
        multiplicationValue=calculateValue(hypo,hypoValue,neededEvidence)
        #falseMultiplicationValue=calculateValue(hypo,'f',evidenceDict)
        variablesDict.update({hypo:hypoValue})
        if parent:
            variablesDict.update(parent.variables)

        variablesDict.update(evidenceDict)

        if parent!= None:
            multiplicationValue*=parent.value

        if items[1]:
            string=""
            for i in items[1]:
                string+=i
            node=Node(items[0]+"/"+string,parent,None,variablesDict,multiplicationValue)
        else:
            node=Node(items[0],parent,None,variablesDict,multiplicationValue)
        #nodeFalse=Node(items[0]+"/"+items[1],parent,None,variablesDictFalse,falseMultiplicationValue)

        if parent:
            parent.children=[node]
        #temp=list(enumeratedList)
        temp=list(enumeratedList[1:])
        calculateProbabilityUsingTree(temp,evidence,node)

    else:

        variablesDictTrue={}
        variablesDictFalse={}
        hypo=items[1]
        evidenceDict=[]
        """
        if items[2]:
            for i in items[2]:
                for e in evidence:
                    e=e.split(" ")
                    if i == e[0]:
                        evidenceDict.update({i:e[1]})
        """
        findParents=parentsDict.get(items[1])
        neededEvidence={}
        if findParents:
            for p in findParents:
                if p in parent.variables:
                    neededEvidence.update({p:parent.variables.get(p)})


        trueMultiplicationValue=calculateValue(hypo,'t',neededEvidence)
        falseMultiplicationValue=calculateValue(hypo,'f',neededEvidence)
        variablesDictTrue.update({hypo:'t'})
        variablesDictFalse.update({hypo:'f'})
        if parent:
            variablesDictTrue.update(parent.variables)
            variablesDictFalse.update(parent.variables)
        variablesDictTrue.update(evidenceDict)
        variablesDictFalse.update(evidenceDict)
        if parent!= None:
            trueMultiplicationValue*=parent.value
            falseMultiplicationValue*=parent.value
        if items[2]:
            string=""
            for i in items[2]:
                string+=i
            nodeTrue=Node(items[1]+"/"+string,parent,None,variablesDictTrue,trueMultiplicationValue)
            nodeFalse=Node(items[1]+"/"+string,parent,None,variablesDictFalse,falseMultiplicationValue)
        else:
            nodeTrue=Node(items[1],parent,None,variablesDictTrue,trueMultiplicationValue)
            nodeFalse=Node(items[1],parent,None,variablesDictFalse,falseMultiplicationValue)

        if parent:
            parent.children=[nodeTrue,nodeFalse]

        #temp=list(enumeratedList)
        temp=list(enumeratedList[1:])
        if parent:
            for child in parent.children:
                calculateProbabilityUsingTree(temp,evidence,child)

        else:
            calculateProbabilityUsingTree(temp,evidence,nodeTrue)
            calculateProbabilityUsingTree(temp,evidence,nodeFalse)


def evaluateEnumeration():
    hypothesis,evidence=takeInputEnumeration()
    return enumerationAsk(hypothesis, evidence,topologicalOrder)

def evalEventToAnswerQuery(sampleList,num,deno,isBoth=False,isPrint=True):

    resultDict={}
    denoSearchDict = genSearchQuery(deno)
    for query in num:
        numSearchDict = genSearchQuery(query)
        queryVariable=query[-1].split(" ")
        result=count(sampleList, numSearchDict, denoSearchDict)
        if isPrint:
          print queryVariable[0],result
        resultDict.update({queryVariable[0]:result})
    if isBoth:
        for query in num:
            tempQuery = query[len(query) - 1]
            arr = tempQuery.split(" ")
            query.remove(tempQuery)
            query.append(arr[0] + " f")
            numSearchDict = genSearchQuery(query)
            print count(sampleList, numSearchDict, denoSearchDict)
    return resultDict


def evaluateQuery():

    codeToExecute=sys.argv[1]
    if codeToExecute !="e":
      numberOfSamples=int(sys.argv[2])


    if codeToExecute== "e":
        evaluateEnumeration()
    elif codeToExecute=="p":
        num, deno = takeInput()
        sampleList=priorSampling(numberOfSamples)
        evalEventToAnswerQuery(sampleList, num, deno, False)
    elif codeToExecute=="r":
        num, deno = takeInput()
        sampleList=rejectionSampling(numberOfSamples,deno)
        evalEventToAnswerQuery(sampleList, num, deno, False)
    elif codeToExecute=="l":
        num, deno = takeInput()
        likeliHoodWeight(numberOfSamples, deno, num, False)





def performExperiment(algo,numberOfSamples,num, deno ,numOfTime=10):

    resultDict={}
    for i in range(numOfTime):
        tempDict={}
        if algo == "e":
            tempDict=evaluateEnumeration()
        elif algo == "p":
            sampleList = priorSampling(numberOfSamples)
            tempDict=evalEventToAnswerQuery(sampleList, num, deno, False,False)

        elif algo == "r":
            sampleList = rejectionSampling(numberOfSamples, deno)
            tempDict=evalEventToAnswerQuery(sampleList, num, deno, False,False)
        elif algo == "l":
            tempDict=likeliHoodWeight(numberOfSamples, deno, num, False,False)

        for key in tempDict:
            if resultDict.__contains__(key):
                list=resultDict[key]
                list.append(tempDict[key])
                resultDict[key]=list
            else:
                resultDict.update({key:[tempDict[key]]})

    for resultKey in resultDict:
        print resultKey,float(sum(resultDict[resultKey]))/float(len(resultDict[resultKey]))

#p prior,r rejection, l lw
def performMultipleExperiment(algo):
    listOfExp=[10,50,100,200,500,1000,10000,100000]
    if algo=="e":
        performExperiment(algo, 1, 0, 0, 1)
    else:
        num, deno = takeInput()

        for i in listOfExp:
            print "====================", i, "===================="
            performExperiment(algo,i,num, deno,10)


performMultipleExperiment("p")
#evaluateQuery()