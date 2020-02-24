from django.db import connection


class classified:
    def all(self):
        with connection.cursor() as cursor:
            cursor.execute("select image_path from classified")
            datas= cursor.fetchall()
            print(datas)
        return datas

    def selected(self,types,numbers):
        with connection.cursor() as cursor:
            # sql=f" SELECT image_path form classified where {a}={b}"
            cursor.execute(f" SELECT image_path form classified where {types}={numbers};")
            datas= cursor.fetchall()
            # datalist.appen(datas)
            # print(datalist)
            return datas

    # def upload(self):
    #     with connection.cursor() as cursor:
    #         sql="""INSERT INTO classified