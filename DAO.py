class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
                        INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?,?,?,?)
                """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def get_next_id(self):
        c = self._conn.cursor()
        c.execute("""
                     SELECT MAX(id) 
                     FROM vaccines 
                        """)
        return c.fetchone()[0] + 1

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

    def get_oldest_line(self):
        c = self._conn.cursor()
        c.execute("""
                             SELECT date, id  
                             FROM vaccines 
                             ORDER BY id ASC LIMIT 1;
                                """)
        return c.fetchone()

    def get_total_inventory(self):
        c = self._conn.cursor()
        c.execute("""
                             SELECT SUM(quantity) 
                             FROM vaccines 
                                """)
        return c.fetchone()


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                        INSERT INTO suppliers (id, name, logistic) VALUES (?,?,?)
                """, [supplier.id, supplier.name, supplier.logistic])

    def get_logistics(self, name):
        c = self._conn.cursor()
        c.execute("""
                             SELECT logistic 
                             FROM suppliers
                             WHERE name = ?
                                """, [name])
        return c.fetchone()

    def get_supplier(self, name):
        c = self._conn.cursor()
        c.execute("""
                             SELECT id 
                             FROM suppliers
                             WHERE name = ?
                                """, [name])
        return c.fetchone()


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
                        INSERT INTO clinics (id, location, demand, logistic) VALUES (?,?,?,?)
                """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def get_vaccines(self, location):
        c = self._conn.cursor()
        c.execute("""
                                     SELECT logistic 
                                     FROM clinics
                                     WHERE location = ?
                                        """, [location])
        return c.fetchone()

    def get_total_demand(self):
        c = self._conn.cursor()
        c.execute("""
                                 SELECT SUM(demand) 
                                 FROM clinics
                                    """)
        return c.fetchone()

    def use_vaccines(self, location, amount):
        self._conn.execute("""
                                UPDATE clinics SET demand=demand-(?) WHERE location=(?)
                        """, [int(amount), location])


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
                INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?,?,?,?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def receive_order(self, logistic_id, amount):
        self._conn.execute("""
                        UPDATE logistics SET count_received=count_received+(?) WHERE id=(?)
                """, [int(amount), logistic_id[0]])

    def send_order(self, logistic_id, amount):
        self._conn.execute("""
                        UPDATE logistics SET count_sent=count_sent+(?) WHERE id=(?)
                """, [int(amount), logistic_id[0]])

    def get_total_receive(self):
        c = self._conn.cursor()
        c.execute("""
                                     SELECT SUM(count_received) 
                                     FROM logistics
                                        """)
        return c.fetchone()

    def get_total_sent(self):
        c = self._conn.cursor()
        c.execute("""
                                     SELECT SUM(count_sent) 
                                     FROM logistics
                                        """)
        return c.fetchone()
