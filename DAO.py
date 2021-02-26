from DTO import Vaccine, Supplier, Clinic, Logistic


# Data Access Objects:


class _Vaccines:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, vaccine):
        self.conn.execute("""
            INSERT INTO vaccines (id, date, supplier, quantity) 
            VALUES (?, ?, ?, ?)""", [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM vaccines WHERE id = ?
            """, [vaccine_id])

        return Vaccine(*cursor.fetchone())

    def update(self, vaccine_id, quantity):
        self.conn.execute("""
            UPDATE vaccines SET quantity = (?) WHERE id = (?)""", [quantity, vaccine_id])

    def delete(self, vaccine_id):
        self.conn.execute("DELETE FROM vaccines WHERE id = ?", [vaccine_id])


class _Suppliers:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, supplier):
        self.conn.execute("""
        INSERT INTO suppliers (id, name, logistic) 
        VALUES (?, ?, ?)""", [supplier.id, supplier.name, supplier.logistic])

    def find(self, supplier_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM suppliers WHERE id = ?
            """, [supplier_id])

        return Supplier(*cursor.fetchone())


class _Clinics:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, clinic):
        self.conn.execute("""
            INSERT INTO clinics (id, location, demand, logistic)
            VALUES (?, ?, ?, ?)""", [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, clinic_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM clinics WHERE id = ?
            """, [clinic_id])

        return Clinic(*cursor.fetchone())

    def update(self, clinic_id, demand):
        self.conn.execute("""
        UPDATE clinics SET demand = (?) WHERE id = (?)""", [demand, clinic_id])


class _Logistics:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, logistic):
        self.conn.execute("""
            INSERT INTO logistics  (id, name, count_sent, count_received)
            VALUES (?, ?, ?, ?)""", [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, logistic_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM logistics WHERE id = ?
            """, [logistic_id])

        return Logistic(*cursor.fetchone())

    # update count_received of logistic with logistic_id
    def update_count_received(self, logistic_id, count_received):
        self.conn.execute("""
            UPDATE logistics SET count_received = (?) WHERE id = (?)""", [count_received, logistic_id])

    # update count_sent of logistic with logistic_id
    def update_count_sent(self, logistic_id, count_sent):
        self.conn.execute("""
            UPDATE logistics SET count_sent = (?) WHERE id = (?)""", [count_sent, logistic_id])