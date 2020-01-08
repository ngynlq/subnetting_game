import time
import os
BIT = 0
CIDR = 1
BIT8 = 2
MASK = 3
class Score:
    def __init__(self,name):
        self._file = name
    def logScore(self,pick,result,run):
        date = time.strftime("%m/%d/%Y")
        if os.path.exists(self._file):
            write_mode = 'a'
        else:
            write_mode = 'w'
        
        reader = open(self._file,write_mode)
        line = date+ ":"+str(pick)+':'+str(result)+":"+str(run)+'\n'
        reader.write(line)
        reader.close()
    def findScore(self):
        correct = {}
        total = {}
        with open(self._file) as f:
            for line in f:
                newLine = line.split(':')
                date,pick,result,run = newLine
                if pick in total:
                    total[pick] = total[pick] + 1
                else:
                    total[pick] = 1
                    correct[pick] = 0
                if int(result) == 1:
                    correct[pick] = correct[pick] + 1
                
        return correct,total
    def printScore(self):
        correct,total = self.findScore()
        print("Culumative Scoring")
        word = ['BIT','CIDR','BIT8','MASK']
        keys = correct.keys()
        for key in keys:
            newkey = int(key)
            print(word[newkey],correct[key],'/',total[key])
                    
                
        
            
            
        
