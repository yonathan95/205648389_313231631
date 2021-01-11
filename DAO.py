# Data Access Objects:
class _Vaccines:
    # constructor DAO _Vaccines.
    def __init__(self, conn):
        self._conn = conn

    # insert new vaccine to _Vaccines.
    def insert(self, vaccine):
        self._conn.execute("""
                        INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?,?,?,?)
                """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])
    #return the next id number available.
    def get_next_id(self):
        c = self._conn.cursor()
        c.execute("""
                     SELECT MAX(id) 
                     FROM vaccines 
                        """)
        return c.fetchone()[0] + 1
    #use the oldest vaccines available. if the quantity is 0 is a specific row , it delete the row form the table.
    def use(self, amount):
        oldest_row = _Vaccines.get_oldest_line(self)
        c = self._conn.cursor()
        c.execute("""
                                     SELECT quantity 
                                     FROM vaccines
                                     WHERE id=(?) 
                                        """,[int(oldest_row[1])])
        num = int(c.fetchone()[0])
        while (int(amount) >= num):
            amount = int(amount) - num
            self._conn.execute("""
                                        DELETE FROM vaccines WHERE id=(?)
                                    """, [oldest_row[1]])
            oldest_row = _Vaccines.get_oldest_line(self)
            c.execute("""
                                                 SELECT quantity 
                                                 FROM vaccines
                                                 WHERE id=(?) 
                                                    """, [int(oldest_row[1])])
            num = int(c.fetchone()[0])
        self._conn.execute("""
                                UPDATE vaccines SET quantity=quantity-(?) WHERE id=(?)
                        """, [int(amount),int(oldest_row[1])])

    # return the id of the row with the oldest date.
    def get_oldest_line(self):
        c = self._conn.cursor()
        c.execute("""
                             SELECT date, id  
                             FROM vaccines 
                             ORDER BY id ASC LIMIT 1;
                                """)
        return c.fetchone()

    # return the sum of all the quantity available.
    def get_total_inventory(self):
        c = self._conn.cursor()
        c.execute("""
                             SELECT SUM(quantity) 
                             FROM vaccines 
                                """)
        return c.fetchone()


class _Suppliers:
    # constructor DAO _Suppliers.
    def __init__(self, conn):
        self._conn = conn

    # insert new supplier to _Suppliers.
    def insert(self, supplier):
        self._conn.execute("""
                        INSERT INTO suppliers (id, name, logistic) VALUES (?,?,?)
                """, [supplier.id, supplier.name, supplier.logistic])
    #return the id of the logistic assisted with the specific supplier.
    def get_logistics(self, name):
        c = self._conn.cursor()
        c.execute("""
                             SELECT logistic 
                             FROM suppliers
                             WHERE name = ?
                                """, [name])
        return c.fetchone()

    # return the name of the supplier assisted with the specific id.
    def get_supplier(self, name):
        c = self._conn.cursor()
        c.execute("""
                             SELECT id 
                             FROM suppliers
                             WHERE name = ?
                                """, [name])
        return c.fetchone()


class _Clinics:
    # constructor DAO _Clinics.
    def __init__(self, conn):
        self._conn = conn

    # insert new clinic to _Clinics.
    def insert(self, clinic):
        self._conn.execute("""
                        INSERT INTO clinics (id, location, demand, logistic) VALUES (?,?,?,?)
                """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])
    #return the id of the logistic assisted with the specific clinic.
    def get_vaccines(self, location):
        c = self._conn.cursor()
        c.execute("""
                                     SELECT logistic 
                                     FROM clinics
                                     WHERE location = ?
                                        """, [location])
        return c.fetchone()
    # return the sum of all the demand.
    def get_total_demand(self):
        c = self._conn.cursor()
        c.execute("""
                                 SELECT SUM(demand) 
                                 FROM clinics
                                    """)
        return c.fetchone()
    # update the demand of a specific clinic.
    def use_vaccines(self, location, amount):
        self._conn.execute("""
                                UPDATE clinics SET demand=demand-(?) WHERE location=(?)
                        """, [int(amount), location])


class _Logistics:
    # constructor DAO _Logistics
    def __init__(self, conn):
        self._conn = conn

    # insert new logistic to _Logistics.
    def insert(self, logistic):
        self._conn.execute("""
                INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?,?,?,?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    # update the count_received of a specific logistic.
    def receive_order(self, logistic_id, amount):
        self._conn.execute("""
                        UPDATE logistics SET count_received=count_received+(?) WHERE id=(?)
                """, [int(amount), logistic_id[0]])

    # update the count_sent of a specific logistic.
    def send_order(self, logistic_id, amount):
        self._conn.execute("""
                        UPDATE logistics SET count_sent=count_sent+(?) WHERE id=(?)
                """, [int(amount), logistic_id[0]])

    # return the sum of all the count_received.
    def get_total_receive(self):
        c = self._conn.cursor()
        c.execute("""
                                     SELECT SUM(count_received) 
                                     FROM logistics
                                        """)
        return c.fetchone()

    # return the sum of all the count_sent.
    def get_total_sent(self):
        c = self._conn.cursor()
        c.execute("""
                                     SELECT SUM(count_sent) 
                                     FROM logistics
                                        """)
        return c.fetchone()
