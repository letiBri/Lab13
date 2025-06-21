from database.DB_connect import DBConnect
from model.driver import Driver


class DAO:

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select distinct(year)
                    from seasons s  """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row["year"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllDrivers():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select d.*
                    from drivers d """
        cursor.execute(query)
        for row in cursor:
            result.append(Driver(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(anno, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select distinct(rs.driverId) 
                    from results rs, (select *
                                        from races r
                                        where r.year=%s) t
                    where t.raceId = rs.raceId and rs.`position` is not null"""
        cursor.execute(query, (anno, ))
        for row in cursor:
            result.append(idMap[row["driverId"]])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(anno, driver1, driver2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select count(*) as peso
                    from(select r.raceId as race, r1.driverId as d1, r1.position as p1, r2.driverId as d2, r2.position as p2
                            from races r, results r1, results r2
                            where r.year = %s and r.raceId = r1.raceId and r.raceId = r2.raceId 
                            and r1.driverId = %s and r2.driverId = %s
                            and r1.position < r2.position and r1.position > 0 and r2.position > 0) t"""
        cursor.execute(query, (anno, driver1.driverId, driver2.driverId))
        for row in cursor:
            result.append(row["peso"])
        cursor.close()
        conn.close()
        return result

