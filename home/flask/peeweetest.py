from  peewee  import  *

db  =  MySQLDatabase ( 'test' ,  user = 'root' ,  passwd = 'root' )

class  Classified ( Model ): 
    with open('home/object_detection/data/classes/coco2.names', 'r') as f:
    #with open('coco2.names', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line=line.replace('\n','')
            locals()[line]= IntegerField (default=0) 
    image_path =  TextField() 
    '''
    person =  IntegerField (default=0) 
    bicycle  =  IntegerField (default=0)
    bicycle2  =  IntegerField (default=0)
    '''

    class  Meta : 
        database  =  db




if __name__ == '__main__':
    Classified.create_table () 


'''
book  =  Book (author = "me" ,  title = 'Peewee is cool' ) 
book . save () 




for  book  in  Book.filter ( author = "me" ): 
    print ( book.title )
'''
