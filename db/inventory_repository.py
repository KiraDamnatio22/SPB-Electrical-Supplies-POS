from datetime import datetime


class InventoryRepository:
    def __init__(self, db):
        self.db = db
        self.cur = db.cur
        self.conn = db.conn

    # =========================
    # ITEMS
    # =========================
    def seed_items_if_empty(self):
        if self.count_items() > 0:
            return

        items = [
            {
                "barcode": "E202601242450001",
                "name": "Welding Rod",
                "category": "Label",
                "price": 120.00,
                "description": "Long Copper Rod for Welding",
                "quantity": 15
            },
            {
                "barcode": "E202601243450002",
                "name": "Access Valve",
                "category": "Scanner",
                "price": 250.00,
                "description": "Long Gold Coated Valve",
                "quantity": 10
            },
            {
                "barcode": "E202601244450003",
                "name": "Silver Rod",
                "category": "Wireless",
                "price": 200.00,
                "description": "Long Rod Coated",
                "quantity": 1
            },
            {
                "barcode": "E202601245450004",
                "name": "Polytape",
                "category": "Sticker",
                "price": 120.00,
                "description": "Long Copper Rod for Welding",
                "quantity": 15
            },
            {
                "barcode": "E202601246450005",
                "name": "Aerotape",
                "category": "Solder",
                "price": 250.00,
                "description": "Long Gold Coated Valve",
                "quantity": 10
            },
            {
                "barcode": "E202601247450006",
                "name": "Tox 12mm",
                "category": "Label",
                "price": 200.00,
                "description": "Long Rod Coated",
                "quantity": 1
            },
            {
                "barcode": "E202601248450007",
                "name": "Screw #6",
                "category": "Scanner",
                "price": 250.00,
                "description": "Long Gold Coated Valve SSSSSSSSSSSSSS",
                "quantity": 10
            },
            {
                "barcode": "E202601249450008",
                "name": "Electrical Tape",
                "category": "Wireless",
                "price": 200.00,
                "description": "Long Rod Coated",
                "quantity": 1
            }
            
        ]

        for item in items:
            self.cur.execute("""
                INSERT INTO items (barcode, name, category, quantity, created_at, price, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item["barcode"],
                item["name"],
                item["category"],
                item["quantity"],
                datetime.now().isoformat(),
                item["price"],
                item["description"]
            ))

        self.conn.commit()

    def get_items_by_category(self, category):
        self.cur.execute("""
            SELECT barcode, name, category, quantity, created_at, price, description
            FROM items
            WHERE category = ?
            ORDER BY name
        """, (category,))
        return self.cur.fetchall()

    def get_all_items(self):
        self.cur.execute("""
            SELECT barcode, name, category, quantity, created_at, price, description
            FROM items
            ORDER BY name
        """)
        return self.cur.fetchall()

    def get_item_by_barcode(self, barcode):
        self.cur.execute("""
            SELECT name, quantity
            FROM items
            WHERE barcode=?
        """, (barcode,))
        return self.cur.fetchone()
    
    def get_item_full(self, barcode):
        self.cur.execute("""
            SELECT barcode, name, category, quantity, price, description
            FROM items
            WHERE barcode=?
        """, (barcode,))
        row = self.cur.fetchone()

        return {
            "barcode": row[0],
            "name": row[1],
            "category": row[2],
            "quantity": row[3],
            "price": row[4],
            "description": row[5]
        }

    def create_item(self, barcode, name, category, price=0, description=""):
        self.cur.execute("""
            INSERT INTO items (barcode, name, category, quantity, created_at, price, description)
            VALUES (?, ?, ?, 0, ?, ?, ?)
        """, (barcode, name, category, datetime.now().isoformat(), price, description))
        self.conn.commit()

    def update_quantity(self, barcode, new_qty):
        self.cur.execute("""
            UPDATE items SET quantity=? WHERE barcode=?
        """, (new_qty, barcode))

    def update_item(self, barcode, data):
        self.cur.execute("""
            UPDATE items
            SET name=?, category=?, price=?, description=?
            WHERE barcode=?
        """, (
            data["name"],
            data["category"],
            data["price"],
            data["description"],
            barcode
        ))
        self.conn.commit()

    # =========================
    # TRANSACTIONS
    # =========================
    def record_transaction(self, barcode, action, qty):
        self.cur.execute("""
            INSERT INTO transactions (barcode, action, qty, timestamp)
            VALUES (?, ?, ?, ?)
        """, (barcode, action, qty, datetime.now().isoformat()))
        self.conn.commit()

    # =========================
    # UTILS
    # =========================
    def count_items(self):
        self.cur.execute("SELECT COUNT(*) FROM items")
        return self.cur.fetchone()[0]
