from RanBlock import BlockCipherRand as rnd
from Crypto.Cipher import AES
from decimal import Decimal
import wave
import ipaddress

class Blockrandom:
    __seed = None
    __entropy = None
    __SourceFileChunks = []
    __sourceIndex = 0
    __ChunkLen = 0
    def __init__(self,SourceFile) -> None:
        """
        sets up RNG system
        Mode settings:
            6 - CTR mode (default)
        """
        self.GetDataChunks(SourceFile)#gets data from sound file
        self.__seed = self.GetChunk() #seeds initials states
        self.__entropy = self.GetChunk()
        self.ReSeed() # reseeds

    def generateRandom(self):
        EncryptData = bytes(self.__entropy,'utf-8')#gets a reading from the sensors
        key = bytes(self.__seed,'utf-8')#gets the key for the cipher (this is the seed value)
        cipher = None
        cipher = AES.new(key,mode=6)#runs the cipher using the seed, in counter mode
        
        ByteRandom = cipher.encrypt(EncryptData)
        Random = (int.from_bytes(ByteRandom,byteorder="little"))#converts the byte to int using order
        self.__entropy = self.GetChunk()
        return Random

    def ReSeed(self):
        random = str(self.generateRandom())#calculates a new seed based on the init seed and a new reading
        newSeed = int(random[0:15])
        self._seed=str(newSeed)# replaces the current seed with the seed passed to function 
    
    def WavToBin(self,sourcefile): # converts wav to binary
        w = wave.open(sourcefile)
        binDat = w.readframes(w.getnframes())
        return binDat

    def GetDataChunks(self,sourceFile):
        
        arr = self.WavToBin(sourceFile)#convets to bin

        stringBlob = str(arr)[3:-1] #removes binary format characters and stores as blob data
        blobLen = len(stringBlob) # finds the leng
        finIndex = (int(blobLen/16))*16 #Removes any remainder
        FinalBlob = stringBlob[:finIndex] # finds the final point
        self.__SourceFileChunks = [FinalBlob[i:i+16] for i in range(0, len(FinalBlob), 16)] # splits into 16 char long chunks
        self.__ChunkLen = len(self.__SourceFileChunks) # notes how long

    def GetChunk(self):
        if(self.__sourceIndex<self.__ChunkLen):#If not at end of data
            Chunk = self.__SourceFileChunks[self.__sourceIndex] # return chunk at this index
            self.__sourceIndex +=1 #iterate
        else:
            self.__sourceIndex = 0 #reset index
            Chunk = self.__SourceFileChunks[self.__sourceIndex]
        return Chunk

    def getRandom(self):

        randGen = str(self.generateRandom()) # returns random number
        appendData = "0."
        ranNum = appendData + randGen
        return Decimal(ranNum) #converts from string to floating point decimal

    def getRanRangeInt(self,min, max):

        """Return int within range

        Args:
            min: min value of return
            max: max value of return
        Returns:
            Integer within range
        """
        min = min-1 # Set outside range to allow for maths to work
        max = max + 1
        Rand = self #sets call
        diff = max-min #calculats the difference
        ranged = Rand.getRandom() #gets a random number in decimal string form
        ranged = (ranged*diff) # calculates the number within the range
        ranged = int(ranged+min)  #adds min to. 
        return ranged
    


class ipRandom:
    __header = None
    __rnd = None
    def __init__(self,header = None,) -> None:
        """
        can generate either entire addresses or a subnet with a header.

        """
        self.__header = header
        self.__rnd = Blockrandom("recording.wav")

    def getIPChunk(self):#generates a 16 bit set
        IPChunk = []
        for i in range(4):
            ran_val = self.__rnd.getRanRangeInt(0,15) # hex is 0-15
            ran_Hex = f'{ran_val:x}' # converts to hex
            IPChunk.append(ran_Hex) # add to list
        out = "".join(IPChunk) #turns list into aaaa form
        return out
    def getIP(self):
        IPList = []#contains the chunks gotten from the loops
        if self.__header == None: # calculate full address
            for i in range(8):
                IPList.append(self.getIPChunk()) 
            ipaddr = ":".join(IPList) # converts list to ip in for of aaaa:aaaa ....
        else:
            for i in range(4): # if header is passed
                IPList.append(self.getIPChunk()) #gets ip chunks and adds to list
            subnet = ":".join(IPList) # converts the subnet 
            ipaddr = self.__header+":"+subnet # adds header
        ip = ipaddress.ip_address(ipaddr) # transforms into a ipaddress using inbuilt method
        ip = ip.compressed # applies compression rules
        return ip

head = "000a:0000:0000:0001"       
ipgen = ipRandom(head)
HeadIP = ipgen.getIP()

print("IP with header:")
print(HeadIP)

ipgen = ipRandom()
fullip = ipgen.getIP()
print("Full IP")
print(fullip)
