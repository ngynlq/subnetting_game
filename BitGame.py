from random import randint,choice
from score import Score
import time
def intToBinStr(number):
    temp = str(bin(int(number)))
    return temp[2:]
def padBits(bits):
    return '0'* (8- len(bits)) + bits
def randomSubnet(bits):
    bitsOff = 32 - bits
    subnet = ''
    subnetStr = '1' * bits + bitsOff * '0'
    for i in range(0,4):
        subnet = subnet + str(int(subnetStr[i*8:(i+1)*8],2)) + '.' 
    return subnet[:len(subnet)-1]
class Generate:
    def __init__(self):
        self.problems = [self.probBit,self.probCIDR,self.prob8Bit,self.probMaskToCIDR]
    #generate 0- 255 to pair with decimal
    def chooseProblem(self,pick):
        if int(pick) == -1:
            random = randint(0,3)
            text,answer = self.problems[random]()
            return random,text,answer
        else:
            text,answer = self.problems[int(pick)]()
            return int(pick),text,answer
    def probBit(self):
        problem,answer = self.genBit(randint(0,255))
        text = 'What is the integer value of ' + str(problem)
        return text,str(answer)
    def probCIDR(self):
        problem,answer = self.genCIDR(randint(1,30))
        text = 'What is the integer value of the mask ' + str(problem)
        return text,str(answer)
    def prob8Bit(self):
        problem,answer = self.gen8bit(randint(1,8))
        text = 'What is the integer value of 2^'+ str(problem)
        return text,str(answer)
    def probMaskToCIDR(self):#int to /
        problem,answer = self.genMaskToCIDR(randomSubnet(randint(1,30)))
        text = 'What is the CIDR value of the subnet mask:' + str(problem)
        return text,str(answer)
    def genBit(self,random):
        answer = random
        problem = bin(answer)
        return (problem,answer)
    #pair find the bit number with given mask
    def genCIDR(self,random):
        bitOns = random#randint(1,30)
        bitOff = 32 - bitOns
        binStr = '1'*bitOns + '0'* bitOff
        answer = str(int(binStr[0:8],2))+'.'+str(int(binStr[8:16],2))+'.'+str(int(binStr[16:24],2))+'.'+str(int(binStr[24:],2))
        return (bitOns,answer)
    #2 to the power of 8
    def gen8bit(self,random):
        numBit = random
        return (random,pow(2,numBit))
    def genMaskToCIDR(self,random):
        strList = random.split('.')
        newList = []
        for byte in strList:
            newList.append(padBits(intToBinStr(byte)))
        maskStr = "".join(newList)
        splitList = maskStr.split('0')
        CIDR = len(splitList[0])
        invalid = False
        if splitList[0] == "":
            invalid = True
            CIDR = -1
        for i in splitList[1:]:
            if i != "":
                invalid = True
                CIDR = -1
        return (random,CIDR)
def main():
    game = Generate()
    score = Score('score.txt')
    mode = input('''What mode do you want to practice on?
                BIT = 0
                CIDR = 1
                BIT8 = 2
                MASK = 3
                Random = -1
                 ''')
    #could be a function
    digit = False
    rounds = 0
    while(not digit):
        rounds = input('How many rounds do you want to play?')
        digit = rounds.isdigit()
    rounds = int(rounds)
    #function end
    
    played = 0  
    correct = 0
    wrong = 0
    while(played < rounds):
        pick,problem,answer = game.chooseProblem(mode)#pull random question
        print(problem)
        start_time = time.time()
        guess = input('>')
        result = 0
        if guess != answer:
            wrong = wrong + 1
            result = 0
        else:
            correct = correct +1
            result = 1
        end_time = time.time()
        work_time = end_time - start_time
        score.logScore(pick,result,work_time)
        print(answer)
        
        played = played + 1
    print('Correct:',correct,'Wrong:',wrong)
    score.printScore()
    x = input('Click to end')
if __name__ == '__main__':
    main()
                
        
                
        

                

