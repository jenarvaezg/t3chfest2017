import nltk
d = {}

with open("dic.txt") as f:
    for line in f:
        
        l = line.split("\t")
        d[l[0]] = int(l[1])
        
tokens = "My dick is huge".split(' ')

acum = 0
cont = 0

for t in tokens:
    cont += 1
    v = d.get(t,0)
    
    acum += v
    acum = acum / cont

print(acum)
