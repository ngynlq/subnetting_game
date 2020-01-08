from math import log
from netfunc import *
import network
#tasks
#create assignment function? no, this way is more readable
#may need to rename mask to dotted4 and define dotted 4
#subnet and ip readable
class Subnet:
	#Subnneting IPv4 just a printing class
	def __init__(self,ip,mask):
		self.__network = network.Network(ip,mask)

	def subByMask(self,mask):
		#To configure the function to iterate over.
		#but can't iterate over the subnet part
		self.__borrow = maskToInt(mask) - self.__network.getIntMask()
		self.__subnets = pow(2,self.__borrow)
		self.__hosts = pow (2,32 - maskToInt(mask))
		self.__subnetMask = network.intToMask((self.__network.getIntMask() + self.__borrow))

	def subByNets(self,number):
		#subnet by the number of desired subnets to be made
		#grabs highest nearest value to the number
		#assumes >0
		cap = 32 - self.__network.getIntMask() - 2
		self.__borrow = near2pow(min(cap,number))
		self.__subnets = pow(2,self.__borrow)
		hosts = 32 - self.__network.getIntMask() - self.__borrow
		self.__hosts = pow(2,hosts) - 2
		self.__subnetMask = network.intToMask((self.__network.getIntMask() + self.__borrow))

	def subByHosts(self,number):
		#fix the number of required minimum hosts
		cap = 32 - self.__network.getIntMask() - 1
		hosts = numOfHosts(min(number,cap))
		self.__hosts = pow(2,hosts) - 2
		self.__borrow = 32 - hosts - self.__network.getIntMask()
		self.__subnets = pow(2,self.__borrow)
		self.__subnetMask = network.intToMask((self.__network.getIntMask() + self.__borrow))
	def subPrecise(self,nets,hosts,hostPri = True):
		#let argparse do net/host checking assume user will be correct here, and adjust extras
		self.__borrow = near2pow(nets)
		hosts = numOfHosts(hosts)
		extra = 32 - self.__network.getIntMask() - self.__borrow - hosts
		if hostPri:
			hosts = hosts + extra
		else:
			self.__borrow = self.__borrow + extra
		self.__hosts = pow(2,hosts)
		self.__subnets = pow(2,self.__borrow)
		self.__subnetMask = network.intToMask((self.__network.getIntMask() + self.__borrow))
	def createSubnet(self,num):
		#for better unittesting/one job
		networkID = self.__network.getBinNetID()
		subnetBin = padBits(intToBinStr(num),self.__borrow)
		newID = networkID + subnetBin
		subnetID = newID + '0' * (32 - len(newID))
		startAdd = bitStrToMask(str(int(subnetID) + 0b1))
		broadcast = newID + '1' * (32 -len(newID))
		endAdd = bitStrToMask(str(int(broadcast) - 0b1))
		subnetStr = bitStrToMask(subnetID)
		broadcastStr = bitStrToMask(broadcast)
		return subnetStr,startAdd,endAdd,broadcastStr
	def printSubnets(self,count=10):
		#prints subnets limit self to simple tasks such as int before giving a list type
		#extract the definition for better testing
		#research storing format 
		#Allow simple export? well, the createsubnet function handles that...
		#printsubnets this one can be replaced by anything.
		limit = int(min(count,self.__subnets))
		for num in range(0,limit):
			subnet,startAdd,endAdd,broadcast = self.createSubnet(num)
			print("SubnetID:{} Mask:{} Range:{} - {} Broadcast {}".format(subnet,self.__subnetMask,startAdd,endAdd,broadcast))