import BitHash
import BitVector

class BloomFilter(object):
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        # Calculate phi 
        phi = (1 - (maxFalsePositive ** (1 / numHashes)))
        
        # Calculate the number of bits needed 
        N = int(numHashes / (1 - (phi ** (1 / numKeys))))
        
        return N
        
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # Initialize private attributes
        self.__bitsNeeded = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        self.__B = BitVector.BitVector(size=self.__bitsNeeded)
        self.__oneBits = 0
        self.__numHashes = numHashes
        self.__maxFalse = maxFalsePositive
        self.__numKeys = numKeys
    
    def insert(self, key):
        for i in range(1, self.__numHashes + 1):
            # Calculate hash value
            hashVal = BitHash.BitHash(key, i) % len(self.__B)
            
            # Increment the count of set bits if the bit was not set previously
            if self.__B[hashVal] == 0:
                self.__oneBits += 1
            
            # Set the bit
            self.__B[hashVal] = 1
    
    def find(self, key):
        for i in range(1, self.__numHashes + 1):
            # Calculate hash value 
            hashVal = BitHash.BitHash(key, i) % len(self.__B)
            
            # If any of the corresponding bits are not set, return False
            if self.__B[hashVal] != 1:
                return False
        
        # If all corresponding bits are set, return True
        return True
       
    def falsePositiveRate(self):
        # Calculate phi 
        phi = (len(self.__B) - self.__oneBits) / len(self.__B)
                
        # Calculate the projected false positive rate
        P = (1 - phi) ** self.__numHashes
        
        return P
    
    def numBitsSet(self):
        # Return the count of set bits
        return self.__oneBits
    

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = 0.05
    
    B = BloomFilter(numKeys, numHashes, maxFalse)
    
    # Read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    fin = open("wordlist.txt")
    for i in range(numKeys):
        line = fin.readline().strip()
        B.insert(line)
    fin.close()
    
    print('Projected false positive rate: ', B.falsePositiveRate())
    
    # count how many numKeys are missing from the Bloom Filter, 
    fin = open('wordlist.txt')
    wordsMissing = 0
    for i in range(numKeys):
        line = fin.readline().strip()
        if not B.find(line):
            wordsMissing += 1
    print('There are ' , wordsMissing, 'words missing from the Bloom Filter')
    
    #count how many of the words can be (falsely) found in the Bloom Filter.
    wordsFound = 0
    for i in range(numKeys):
        line = fin.readline().strip()
        if B.find(line):
            wordsFound += 1

    print('Percentage of false positves:', wordsFound / numKeys)
    
if __name__ == '__main__':
    __main()
