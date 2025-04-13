from bitarray import bitarray

s="" #To store the read text 

c=[] #For storing the nodes that contains the characters and their frequencies

#Class for the nodes 
class N:
    def __init__(self, value, c):
        self.value = value
        self.c=c
        self.code=None
        self.left = None  
        self.right = None

    def __repr__(self):
        return f"({self.c}, {self.value}, {self.code})"

#function to read from a file the text to be ecoded and store it in s
def readFromFile():
    global s
    with open("text.txt","r") as fr:
        s=fr.read()


#computing occurences
def compute_occ():
    i=0
    for i in range(len(s)):
        flag=1
        j=0
        for j in range(len(c)):
            if (s[i]==c[j].c):
                flag=0
        if flag==1:
            temp=N(s.count(s[i]),s[i])
            c.append(temp)



#sorting an array in ascending order

def arrange(index,array):
    array[index:]=sorted(array[index:],key=lambda n: n.value)
    return array

#creating the tree for the nodes 
def createTree(c_second):
    i=0
    while(i!=len(c_second)-1):
        temp=N(c_second[i].value+c_second[i+1].value,None)
        temp.left,temp.right=c_second[i],c_second[i+1]
        c_second[i+1]=temp
        c_second=arrange(i,c_second)
        i=i+1
    return c_second[i]
        
#printing the tree
def printTree(root):
    if root==None:
        return
    else:
        print(root)
        printTree(root.left)
        printTree(root.right)


#encoding the each character in the tree 
def encode(root,s,result):
    if root==None:
        return
    elif root.left==None and root.right==None:
        root.code=s
        result.append(root)
    else:
        encode(root.left,s+"0",result)
        encode(root.right,s+"1",result)
#Conevrting the codes to binary and writing them to a file
def writeToFile(result):
    encoding_map={node.c : node.code for node in result}
    bitstream=bitarray()
    for character in s:
        bitstream.extend(encoding_map[character])
    with open("result.bin","wb") as fw:
        bitstream.tofile(fw)
    return bitstream

#decoding the binary file
def decode(bitstream,root):
    decoded=""
    node=root
    for bit in bitstream:
        if bit == 0:
            node=node.left
        else:
            node=node.right
        if node.left==None and node.right==None:
            decoded+=node.c
            node=root
    return decoded

#writing the decoded text to a file
def writeDecoded(decoded):
    with open("decoded.txt","w") as fw:
        fw.write(decoded)

#main
if __name__=="__main__":
    readFromFile()
    compute_occ()
    c_second=arrange(0,c)
    root=createTree(c_second)
    result=[]
    encode(root,"",result)
    bitstream=bitarray()
    bitstream=writeToFile(result)
    decoded=decode(bitstream,root)
    writeDecoded(decoded)
    
    
    


