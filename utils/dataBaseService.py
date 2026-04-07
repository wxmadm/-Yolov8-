from pymysql.cursors import DictCursor
from twisted.enterprise import adbapi
import pymysql

settings = {
    "MYSQL_HOST":"localhost",
    "MYSQL_DBNAME":"cardatabase",
    "MYSQL_USER":"root",
    "MYSQL_PASSWD":"123456",
    "MYSQL_CHARSET":"utf8",
    "MYSQL_PORT":3306
}

class ChaoSu:
    tableName = "chaosu"

    def __init__(self):
        self.id=""
        self.num=""
        self.time=""
        self.speed=""
        self.local=""


class DataBaseService(object):
    single = None

    def __new__(cls, *args, **kwargs):
        if DataBaseService.single is not None:
            return DataBaseService.single
        return super().__new__(cls)

    def __init__(self,dbpool):
        self.dbpool = dbpool
        DataBaseService.single = self
        self.dbpool.start()

    @classmethod
    def connect(cls,settings):
        config = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset=settings['MYSQL_CHARSET'],
            port=settings['MYSQL_PORT'],
            cursorclass=DictCursor,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **config)


        return cls(dbpool)

    @classmethod
    def getKeyValues(cls,data):
        keys = data.__dict__
        keysL=[]
        values=[]
        for key,value in keys.items():
            if not value:
                continue
            keysL.append(key)
            values.append(value)
        return keysL,values

    @classmethod
    def get_sql(cls,table,keys,values):
        print(values)
        sql = "INSERT INTO %s (%s) VALUE (%s)" % (table,",".join(keys),",".join(["'{0}'".format(cell) for cell in values]))
        return sql

    def insert_one(self,cursor,table,result):
        keysL , values = DataBaseService.getKeyValues(result)
        sql = DataBaseService.get_sql(table,keysL,values)
        print(sql)

        cursor.execute(sql) 


    def insert_error(self,result):
        print("写入失败"+result)


    def insertToList(self,chaosu:ChaoSu):
        query = self.dbpool.runInteraction(self.insert_one,chaosu.tableName,chaosu)
        query.addErrback(self.insert_error,chaosu)
        print("ok")



    @classmethod
    def starRun(cls):
        print("DataBaseService.connect(settings):")
        return DataBaseService.connect(settings)
