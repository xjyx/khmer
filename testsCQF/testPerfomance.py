import sys
from khmer import QFCounttable, Counttable

def help():
    print("Usage : python3 testPerformance.py <inputPrefix> <SketchSize>  < --cqf | --cm >")
    print("   <inputPrefix> Prefix of the files generated by generateSeq.py ")
    print("   <SketchSize> The size assigned to the sketch will be approx equal to  2^SketchSize ")
    print("   --cqf to use QF Counttable and --cm to use CountMin sketch")
    print("Results will be printed in case of sucess to the standard output")

if len(sys.argv)!=4 or  sys.argv[1] in ['-h','--h', '--help' ]:
    help()
    exit(0)



inputPrefix=sys.argv[1]
Gold=open(inputPrefix+'.gold')
dataset=open(inputPrefix+'.dat')
NonExisted=open(inputPrefix+'.none.dat')
testCQF=sys.argv[3]=='--cqf'
Sizes=[int(sys.argv[2])] #cqf
#Sizes=[6,7,8,9,10,11,12] #countmin
counterName='Unknown'
for size in Sizes:
    if testCQF:
        size=2**size
        counter=QFCounttable(20,size)
        counterName='CQF'
    else:    
        size=2**(size-2)
        counter=Counttable(20,size,4)
        size*=4
        counterName='CM'
    try:
        for kmer in dataset:
            kmer=kmer.strip()
            counter.count(kmer)
    except:
        print(size,"FAILED")

    countingError=0
    Error=[]
    for l in Gold:
        k,count=l.strip().split("\t")
        count=int(count)
        res=abs(counter.get(k)-count)
        countingError+=res
        Error.append(res)
        
    countingNonExist=0
    falseNonExist=0
    NonExistError=[]
    for k in NonExisted:
        res=counter.get(k.strip())
        countingNonExist+=res
        falseNonExist+=(res!=0)
        NonExistError.append(res)

    print(counterName,size,countingError,countingNonExist,falseNonExist)
    print(",".join([str(a) for a in Error]))
    print(",".join([str(a) for a in NonExistError]))

