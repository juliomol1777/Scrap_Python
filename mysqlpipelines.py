import pymysql
from twisted.enterprise import adbapi


class MysqlPipelineTwo(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):  

        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor
        )
        
        dbpool = adbapi.ConnectionPool('pymysql',**adbparams)
        
        return cls(dbpool)

    def process_item(self,item,spider):
        
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addCallback(self.handle_error)

    def do_insert(self,cursor,item):
        
        insert_sql = """
        insert into relatos(titulo,autor,categoria,texto) VALUES(%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql,(item['titulo'],item['autor'],item['categoria'],item['texto']))
        return item

    def handle_error(self,failure):
        if failure:
            print(failure)

