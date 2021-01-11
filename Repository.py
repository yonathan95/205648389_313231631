import atexit
import sqlite3

from DAO import _Vaccines, _Suppliers, _Clinics, _Logistics
from DTO import Vaccine


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE vaccines (
            id       INTEGER        PRIMARY KEY,
            date     DATE           NOT NULL,
            supplier INTEGER        REFERENCES suppliers(id),
            quantity INTEGER        NOT NULL 
        );

        CREATE TABLE suppliers (
            id       INTEGER        PRIMARY KEY,
            name     VARCHAR(50)    NOT NULL,
            logistic INTEGER        REFERENCES logistics(id)
        );

        CREATE TABLE clinics (
            id         INTEGER        PRIMARY KEY,
            location   VARCHAR(50)    NOT NULL,
            demand     INTEGER        NOT NULL,
            logistic   INTEGER        REFERENCES logistics(id) 
        );
        
        CREATE TABLE logistics (
            id              INTEGER        PRIMARY KEY,
            name            VARCHAR(50)    NOT NULL,
            count_sent      INTEGER        NOT NULL,
            count_received  INTEGER        NOT NULL
        );
    """)

    def send_shipment(self, line):
        _Vaccines.use(self, line[1])
        logistic_id = _Clinics.get_vaccines(self, line[0])
        _Clinics.use_vaccines(self, line[0], line[1])
        _Logistics.send_order(self, logistic_id, line[1])

    def receive_shipment(self, line):
        logistic_id = _Suppliers.get_logistics(self, line[0])
        _Logistics.receive_order(self, logistic_id, line[1])
        v_id = _Vaccines.get_next_id(self)
        line = [v_id, line[2], logistic_id[0], line[1]]
        vaccine = Vaccine(line)
        _Vaccines.insert(self, vaccine)

    def summary(self):
        total_inventory = _Vaccines.get_total_inventory(self)
        total_demand = _Clinics.get_total_demand(self)
        total_receive = _Logistics.get_total_receive(self)
        total_sent = _Logistics.get_total_sent(self)
        output = "{},{},{},{}\n".format(total_inventory[0], total_demand[0], total_receive[0], total_sent[0])
        return output
