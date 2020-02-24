from peeweetest import Classified


with open('data.txt','r') as f:
    output = f.read()


output=output.split('\n')
output.pop()
#print(output)
'''
for item in output:
	element=item.split(',')
	sort  =  Classified ( title = element[1] ) 
	sort . save () 
'''
test={'person':99,'bicycle':4}
sort  =  Classified (**test ) 
sort . save () 


print('************************')
#print(Book.select())

#record=Book.get(author='who cares')
#record.delete_instance()
#print(record.title)
#print(Book.get(author='who cares'))
#record.delete_instance()
#print(record.title)
'''
myit = iter(Classified.filter ( person = 0 ))
print(next(myit).bicycle)
print(next(myit).bicycle)
'''


print('***************************')
for  book  in  Classified.filter ( person= 0): 
	pass
	#print ( book.title )


print('****************')
a=[sort.bicycle for sort in Classified.filter(person=0)]
#print(a)

