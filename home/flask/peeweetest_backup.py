import peewee
from  peewee  import  *

db  =  MySQLDatabase ( 'test' ,  user = 'root' ,  passwd = 'root' )

class  Book ( peewee.Model ): 
    author  =  peewee.CharField () 
    title  =  peewee.TextField ()

    class  Meta : 
        database  =  db




if __name__ == '__main__':
    Book.create_table () 


'''
book  =  Book (author = "me" ,  title = 'Peewee is cool' ) 
book . save () 




for  book  in  Book.filter ( author = "me" ): 
    print ( book.title )
'''
