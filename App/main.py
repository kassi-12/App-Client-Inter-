import eel
import sqlite3
import os
import logging
import webview
import datetime
from collections import defaultdict
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Eel
eel.init("web")

# Get the path to the database
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'web', 'database', 'restaurant.db'))
print(f"Database path: {db_path}")

# Function to add a user
@eel.expose
def add_user(username, email, password, first_name, last_name, gender, phone, bio,group_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (username, email, password, first_name, last_name, gender, phone, bio, group_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, password, first_name, last_name, gender, phone, bio, group_id))

        conn.commit()
        logging.info(f"User {username} added successfully!")
        return "User added successfully!"
    except sqlite3.IntegrityError:
        logging.warning("Email already exists!")
        return "Email already exists!"
    except Exception as e:
        logging.error(f"An error occurred while adding user {username}: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()

# Function to fetch users
@eel.expose
def fetch_users():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id,username, email, first_name, last_name, phone,group_id FROM users')
        users = cursor.fetchall()
        logging.info("Users fetched successfully!")
        return users
    except Exception as e:
        logging.error(f"An error occurred while fetching users: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()
@eel.expose
def fetch_userbyid(user_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, first_name, last_name, gender, phone, bio FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        logging.info(f"User {user_id} fetched successfully!")
        return user
    except Exception as e:
        logging.error(f"An error occurred while fetching user {user_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

@eel.expose
def update_user(user_id, username, email, password, first_name, last_name, gender, phone, bio,group_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users
        SET username = ?, email = ?, password = ?, first_name = ?, last_name = ?, gender = ?, phone = ?, bio = ?, group_id = ?
        WHERE id = ?
        ''', (username, email, password, first_name, last_name, gender, phone, bio, group_id, user_id))

        conn.commit()
        logging.info(f"User {user_id} updated successfully!")
        return True
    except Exception as e:
        logging.error(f"An error occurred while updating user {user_id}: {e}")
        return False
    finally:
        if conn:
            conn.close()
@eel.expose
def delete_user(id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id=?', (id,))
        conn.commit()
        logging.info(f"User with ID {id} deleted successfully!")
        return "User deleted successfully!"
    except Exception as e:
        logging.error(f"An error occurred while deleting user with ID {id}: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()
@eel.expose
def add_table(table_name, capacity, availability, status):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tables (table_name, capacity, availability, status)
            VALUES (?, ?, ?, ?)
        ''', (table_name, capacity, availability, status))
        conn.commit()
        logging.info(f"Table {table_name} added successfully!")
        return "Table added successfully!"
    except sqlite3.IntegrityError:
        logging.warning("Table already exists!")
        return "Table already exists!"
    except Exception as e:
        logging.error(f"An error occurred while adding table {table_name}: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()
@eel.expose
def fetch_tables():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, table_name, capacity, availability, status FROM tables')
        tables = cursor.fetchall()
        logging.info("Tables fetched successfully!")
        return tables
    except Exception as e:
        logging.error(f"An error occurred while fetching tables: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()

@eel.expose
def update_table(table_id, table_name, capacity, availability, status):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tables
            SET table_name = ?, capacity = ?, availability = ?, status = ?
            WHERE id = ?
        ''', (table_name, capacity, availability, status, table_id))
        conn.commit()
        logging.info(f"Table {table_name} updated successfully!")
        return "Table updated successfully!"
    except Exception as e:
        logging.error(f"An error occurred while updating table {table_name}: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()
# Function to delete a table
@eel.expose
def delete_table(id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tables WHERE id=?', (id,))
        conn.commit()
        logging.info(f"Table with ID {id} deleted successfully!")
        return "Table deleted successfully!"
    except Exception as e:
        logging.error(f"An error occurred while deleting table with ID {id}: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()

# Function to fetch categories
@eel.expose
def fetch_categorys():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, status FROM category')
        categories = cursor.fetchall()
        logging.info("Categories fetched successfully!")
        return categories
    except Exception as e:
        logging.error(f"An error occurred while fetching categories: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Function to add a category
@eel.expose
def add_category(name, status):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO category (name, status) VALUES (?, ?)', (name, status))
        conn.commit()
        logging.info(f"Category {name} added successfully!")
        return "Category added successfully!"
    except sqlite3.IntegrityError:
        logging.warning(f"Category with name '{name}' already exists.")
        return "Category with this name already exists."
    except Exception as e:
        logging.error(f"An error occurred while adding category: {e}")
        return "An error occurred while adding the category."
    finally:
        if conn:
            conn.close()

# Function to update a category
@eel.expose
def update_category(id, name, status):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE category SET name = ?, status = ? WHERE id = ?', (name, status, id))
        conn.commit()
        logging.info(f"Category with ID {id} updated successfully!")
        return "Category updated successfully!"
    except Exception as e:
        logging.error(f"An error occurred while updating category: {e}")
        return "An error occurred while updating the category."
    finally:
        if conn:
            conn.close()

# Function to delete a category
@eel.expose
def delete_category(id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM category WHERE id = ?', (id,))
        conn.commit()
        logging.info(f"Category with ID {id} deleted successfully!")
        return "Category deleted successfully!"
    except Exception as e:
        logging.error(f"An error occurred while deleting category: {e}")
        return "An error occurred while deleting the category."
    finally:
        if conn:
            conn.close()
# Function to fetch groups
@eel.expose
def fetch_groups():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, group_name FROM groups')
        groups = cursor.fetchall()
        logging.info("Groups fetched successfully!")
        return groups
    except Exception as e:
        logging.error(f"An error occurred while fetching groups: {e}")
        return []
    finally:
        if conn:
            conn.close()
@eel.expose
def add_group(group_name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO groups (group_name) VALUES (?)', (group_name,))
        conn.commit()
        logging.info(f"Group '{group_name}' added successfully!")
        return "Group added successfully!"
    except sqlite3.IntegrityError:
        logging.warning(f"Group with name '{group_name}' already exists.")
        return "Group with this name already exists."
    except Exception as e:
        logging.error(f"An error occurred while adding group: {e}")
        return "An error occurred while adding the group."
    finally:
        if conn:
            conn.close()
# Function to fetch users by group ID
@eel.expose
def fetch_users_by_group(group_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, email, first_name, last_name, phone
            FROM users
            WHERE group_id = ?
        ''', (group_id,))
        users = cursor.fetchall()
        logging.info(f"Users for Group ID {group_id} fetched successfully!")
        return users
    except Exception as e:
        logging.error(f"An error occurred while fetching users for Group ID {group_id}: {e}")
        return []
    finally:
        if conn:
            conn.close()
# Function to update a group
@eel.expose
def update_group(id, group_name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE groups SET group_name = ? WHERE id = ?', (group_name, id))
        conn.commit()
        logging.info(f"Group with ID {id} updated successfully!")
        return "Group updated successfully!"
    except Exception as e:
        logging.error(f"An error occurred while updating group: {e}")
        return "An error occurred while updating the group."
    finally:
        if conn:
            conn.close()

# Function to delete a group
@eel.expose
def delete_group(id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM groups WHERE id = ?', (id,))
        conn.commit()
        logging.info(f"Group with ID {id} deleted successfully!")
        return "Group deleted successfully!"
    except Exception as e:
        logging.error(f"An error occurred while deleting group: {e}")
        return "An error occurred while deleting the group."
    finally:
        if conn:
            conn.close()



@eel.expose
def add_order_items(order_id, order_items):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for item in order_items:
            cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, item_total) VALUES (?, ?, ?, ?)',
                           (order_id, item['productID'], item['quantity'], item['itemTotal']))
        conn.commit()
        logging.info("Order items added successfully!")
        return True
    except Exception as e:
        conn.rollback()
        logging.error(f"An error occurred while adding order items: {e}")
        return False
    finally:
        if conn:
            conn.close()

@eel.expose
def fetch_orders():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()
        logging.info("Orders fetched successfully!")
        return orders
    except Exception as e:
        logging.error(f"An error occurred while fetching orders: {e}")
        return []
    finally:
        if conn:
            conn.close()
@eel.expose
def fetch_orders_paid():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT order_time,net_amount FROM orders WHERE status="Paid"')
        orders = cursor.fetchall()
        logging.info("Orders fetched successfully!")
        return orders
    except Exception as e:
        logging.error(f"An error occurred while fetching orders: {e}")
        return []
    finally:
        if conn:
            conn.close()
@eel.expose
def fetch_orders_pdf():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id,net_amount,status FROM orders')
        orders = cursor.fetchall()
        logging.info("Orders fetched successfully!")
        return orders
    except Exception as e:
        logging.error(f"An error occurred while fetching orders: {e}")
        return []
    finally:
        if conn:
            conn.close()
@eel.expose
def update_order(id, method, status):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE orders SET method=?, status=? WHERE id=?', (method, status, id))
        conn.commit()
        logging.info("Order updated successfully!")
        return "Order updated successfully!"
    except Exception as e:
        logging.error(f"An error occurred while updating order: {e}")
        return f"Error: {e}"
    finally:
        if conn:
            conn.close()

@eel.expose
def add_order(table_id, user_id, gross_amount, s_charge, vat, discount, net_amount):
   
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO orders (table_id, user_id, gross_amount, s_charge, vat, discount, net_amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, "In Progress")
        ''', (table_id, user_id, gross_amount, s_charge, vat, discount, net_amount))
        
        order_id = cursor.lastrowid
        conn.commit()
        
        logging.info(f"Order {order_id} added successfully!")
        
        return order_id
    
    except sqlite3.Error as e:
        logging.error(f"SQLite error occurred: {e}")
        return None
    
    except Exception as e:
        logging.error(f"An error occurred while adding order: {e}")
        return None
    
    finally:
        if conn:
            conn.close()

@eel.expose
def download_order(id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.id, t.table_name, u.username, o.gross_amount, o.s_charge, o.vat, o.discount, o.net_amount, o.method, o.status
            FROM orders o
            INNER JOIN tables t ON o.table_id = t.id
            INNER JOIN users u ON o.user_id = u.id
            WHERE o.id=?
        ''', (id,))
        order = cursor.fetchone()
        
        if order:
            order_id, table_name, username, gross_amount, s_charge, vat, discount, net_amount, method, status = order
            
            order_data = (
                f"Order Number: {order_id}\n"
                f"Table Name: {table_name}\n"
                f"User Name: {username}\n"
                f"Gross Amount: {gross_amount}\n"
                f"S-Charge: {s_charge}\n"
                f"VAT: {vat}\n"
                f"Discount: {discount}\n"
                f"Net Amount: {net_amount}\n"
                f"Method: {method}\n"
                f"Status: {status}"
            )
            
            documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')
            file_path = os.path.join(documents_folder, f"order_{id}.txt")
            
            with open(file_path, "w") as file:
                file.write(order_data)
            
            logging.info(f"Order {id} downloaded successfully!")
            return file_path
        else:
            logging.error(f"No order found with ID: {id}")
            return None
    except Exception as e:
        logging.error(f"An error occurred while downloading order: {e}")
        return None
    finally:
        if conn:
            conn.close()
@eel.expose
def fetch_orders_status():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE status IN ("In Progress", "Not Paid")')
        orders = cursor.fetchall()
        logging.info("Orders fetched successfully!")
        logging.info(f"Fetched orders: {orders}")  # Log fetched orders for debugging
        return orders
    except Exception as e:
        logging.error(f"An error occurred while fetching orders: {e}")
        return []
    finally:
        if conn:
            conn.close()
@eel.expose
def fetch_company_settings():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM company WHERE id = 1')  # Assuming there's only one row for company settings
        settings = cursor.fetchone()
        logging.info("Company settings fetched successfully!")
        return settings
    except Exception as e:
        logging.error(f"An error occurred while fetching company settings: {e}")
        return None
    finally:
        if conn:
            conn.close()

@eel.expose
def insert_company_settings(settings):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO company (name, language, theme, restaurant_name, address, phone, currency, timezone, tax_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', settings)
        conn.commit()
        logging.info("Company settings inserted successfully!")
    except Exception as e:
        logging.error(f"An error occurred while inserting company settings: {e}")
    finally:
        if conn:
            conn.close()

@eel.expose
def update_company_settings(settings):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE company
            SET name = ?, language = ?, theme = ?, restaurant_name = ?, address = ?, phone = ?, currency = ?, timezone = ?, tax_rate = ?
            WHERE id = 1
        ''', settings)
        conn.commit()
        logging.info("Company settings updated successfully!")
    except Exception as e:
        logging.error(f"An error occurred while updating company settings: {e}")
    finally:
        if conn:
            conn.close()
@eel.expose
def get_table_name_by_id(table_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT table_name FROM tables WHERE id = ?', (table_id,))
        table_name = cursor.fetchone()
        logging.info(f"Table name for ID {table_id} fetched successfully!")
        return table_name[0] if table_name else None
    except Exception as e:
        logging.error(f"An error occurred while fetching table name for ID {table_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()
# Function to calculate total earnings for the current year
@eel.expose
def fetch_group_by_id(group_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT group_name FROM groups WHERE id = ?', (group_id,))
        group_name = cursor.fetchone()
        logging.info("Group fetched successfully!")
        return group_name[0] if group_name else 'Unknown'
    except Exception as e:
        logging.error(f"An error occurred while fetching group: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()



@eel.expose
def add_stock(item_name, quantity, unit, price_per_unit):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO stock (item_name, quantity, unit, price_per_unit)
        VALUES (?, ?, ?, ?)
        ''', (item_name, quantity, unit, price_per_unit))

        conn.commit()
        logging.info(f"Stock item '{item_name}' added successfully!")
        return "Stock item added successfully!"
    except sqlite3.IntegrityError:
        logging.warning("Stock item already exists!")
        return "Stock item already exists!"
    except Exception as e:
        logging.error(f"An error occurred while adding stock item '{item_name}': {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()

@eel.expose
def fetch_stock():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT id, item_name, quantity, unit, price_per_unit
        FROM stock
        ''')
        stock_items = cursor.fetchall()
        logging.info("Stock items fetched successfully!")
        return stock_items
    except Exception as e:
        logging.error(f"An error occurred while fetching stock items: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()

@eel.expose
def update_stock(stock_id, item_name, quantity, unit, price_per_unit):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Fetch current stock details
        cursor.execute('''
        SELECT quantity, price_per_unit
        FROM stock
        WHERE id = ?
        ''', (stock_id,))
        stock_item = cursor.fetchone()

        if stock_item:
            current_quantity, current_price_per_unit = stock_item

            # Calculate new quantity
            new_quantity = current_quantity + int(quantity)

            # Ensure quantity does not go negative
            if new_quantity < 0:
                return "Quantity cannot be negative!"

            # Calculate new price based on weighted average
            total_cost = (current_quantity * current_price_per_unit) + (int(quantity) * float(price_per_unit))
            new_price_per_unit = total_cost / new_quantity if new_quantity != 0 else 0

            # Update stock item with new values
            cursor.execute('''
            UPDATE stock
            SET item_name = ?, quantity = ?, unit = ?, price_per_unit = ?
            WHERE id = ?
            ''', (item_name, new_quantity, unit, new_price_per_unit, stock_id))

            conn.commit()
            logging.info(f"Stock item with ID {stock_id} updated successfully!")
            return "Stock item updated successfully!"
        else:
            return "Stock item not found!"
    except Exception as e:
        logging.error(f"An error occurred while updating stock item with ID {stock_id}: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()

@eel.expose
def delete_stock(stock_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM stock WHERE id = ?', (stock_id,))
        conn.commit()
        logging.info(f"Stock item with ID {stock_id} deleted successfully!")
        return "Stock item deleted successfully!"
    except Exception as e:
        logging.error(f"An error occurred while deleting stock item with ID {stock_id}: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()

@eel.expose
def fetch_analysis_data():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Fetch total earnings of the year
        cursor.execute('SELECT SUM(net_amount) FROM orders WHERE strftime("%Y", order_time) = strftime("%Y", "now") and status="Paid"')
        total_earnings = cursor.fetchone()[0] or 0

        # Fetch total paid orders of the month
        cursor.execute('SELECT COUNT(*) FROM orders WHERE status="Paid"')
        total_paid_orders = cursor.fetchone()[0] or 0

        # Fetch total food products
        cursor.execute('SELECT COUNT(*) FROM products')
        total_food_products = cursor.fetchone()[0] or 0

        # Fetch total food categories
        cursor.execute('SELECT COUNT(*) FROM category')
        total_food_category = cursor.fetchone()[0] or 0

        # Fetch total unpaid orders
        cursor.execute('SELECT COUNT(*) FROM orders WHERE status="Not Paid"')
        total_unpaid_orders = cursor.fetchone()[0] or 0

        # Fetch total orders
        cursor.execute('SELECT COUNT(*) FROM orders')
        total_orders = cursor.fetchone()[0] or 0
        
        # Calculate percentages (example calculation, you can adjust as needed)
        total_earnings_percentage = (total_earnings / 100000) * 100
        total_paid_orders_percentage = (total_paid_orders / 1000) * 100
        total_food_products_percentage = (total_food_products / 5000) * 100
        total_food_category_percentage = (total_food_category / 100) * 100
        total_unpaid_orders_percentage = (total_unpaid_orders / 1000) * 100
        total_orders_percentage = (total_orders / 1000) * 100

        data = {
            "totalEarnings": total_earnings,
            "totalPaidOrders": total_paid_orders,
            "totalFoodProducts": total_food_products,
            "totalFoodCategory": total_food_category,
            "totalUnPaidOrders": total_unpaid_orders,
            "totalOrders": total_orders,
            "totalEarningsPercentage": total_earnings_percentage,
            "totalPaidOrdersPercentage": total_paid_orders_percentage,
            "totalFoodProductsPercentage": total_food_products_percentage,
            "totalFoodCategoryPercentage": total_food_category_percentage,
            "totalUnPaidOrdersPercentage": total_unpaid_orders_percentage,
            "totalOrdersPercentage": total_orders_percentage
        }

        return data
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {}
# Function to fetch products
@eel.expose
def fetch_products():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, category_id, price, status, description FROM products')
        products = cursor.fetchall()
        logging.info("Products fetched successfully!")
        return products
    except Exception as e:
        logging.error(f"An error occurred while fetching products: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Function to add a product
@eel.expose
def add_product(name, category_id, price, status, description):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO products (name, category_id, price, status, description)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, category_id, price, status, description))

        conn.commit()
        logging.info(f"Product {name} added successfully!")
        return "Product added successfully!"
    except sqlite3.IntegrityError:
        logging.warning("Product already exists!")
        return "Product already exists!"
    except Exception as e:
        logging.error(f"An error occurred while adding product {name}: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()

# Function to update a product
@eel.expose
def update_product(id, name, category_id, price, status, description):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE products
        SET name = ?, category_id = ?, price = ?, status = ?, description = ?
        WHERE id = ?
        ''', (name, category_id, price, status, description, id))

        conn.commit()
        logging.info(f"Product with ID {id} updated successfully!")
        return "Product updated successfully!"
    except Exception as e:
        logging.error(f"An error occurred while updating product {id}: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()

# Function to delete a product
@eel.expose
def delete_product(id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (id,))
        conn.commit()
        logging.info(f"Product with ID {id} deleted successfully!")
        return "Product deleted successfully!"
    except Exception as e:
        logging.error(f"An error occurred while deleting product {id}: {e}")
        return f"An error occurred: {e}"
    finally:
        if conn:
            conn.close()
@eel.expose
def fetch_product_by_id(product_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()  
        logging.info(f"Fetched product with ID {product_id} successfully!")
        return product
    except Exception as e:
        logging.error(f"Error fetching product with ID {product_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()
@eel.expose
def check_login(username, password):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, group_id FROM users WHERE email = ? AND password = ?', (username, password))
        user_data = cursor.fetchone()

        if user_data:
            logging.info(f"User {username} logged in successfully!")
            user_id, group_id = user_data
            return {"success": True, "user_id": user_id, "group_id": group_id}
        else:
            logging.warning(f"Invalid login attempt for user {username}")
            return {"success": False}
    except Exception as e:
        logging.error(f"An error occurred while checking login: {e}")
        return {"success": False}
    finally:
        if conn:
            conn.close()
@eel.expose
def generate_pdf_report(orders, users, groups, categories, products, tables, stock, company):
    try:
        documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')
        pdf_path = os.path.join(documents_folder, 'report.pdf')

        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Add Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 50, "Annual Report")

        # Initialize y position for text placement
        y = height - 80

        # Add Orders if not None
        if orders is not None:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y, "Orders:")
            c.setFont("Helvetica", 10)
            y -= 20
            for order in orders:
                c.drawString(30, y, f"Order ID: {order[0]}, Amount: {order[1]}, Status: {order[2]}")
                y -= 20
        
        # Add Users if not None
        if users is not None:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y, "Users:")
            c.setFont("Helvetica", 10)
            y -= 20
            for user in users:
                c.drawString(30, y, f"User ID: {user[0]}, Username: {user[1]}")
                y -= 20

        # Add Groups if not None
        if groups is not None:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y, "Groups:")
            c.setFont("Helvetica", 10)
            y -= 20
            for group in groups:
                c.drawString(30, y, f"Group ID: {group[0]}, Group Name: {group[1]}")
                y -= 20

        # Add Categories if not None
        if categories is not None:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y, "Categories:")
            c.setFont("Helvetica", 10)
            y -= 20
            for category in categories:
                c.drawString(30, y, f"Category ID: {category[0]}, Category Name: {category[1]}")
                y -= 20

        # Add Products if not None
        if products is not None:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y, "Products:")
            c.setFont("Helvetica", 10)
            y -= 20
            for product in products:
                c.drawString(30, y, f"Product ID: {product[0]}, Product Name: {product[1]}")
                y -= 20

        # Add Tables if not None
        if tables is not None:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y, "Tables:")
            c.setFont("Helvetica", 10)
            y -= 20
            for table in tables:
                c.drawString(30, y, f"Table ID: {table[0]}, Table Name: {table[1]}, Capacity: {table[2]}, Availability: {table[3]}")
                y -= 20

        # Add Stock if not None
        if stock is not None:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y, "Stock:")
            c.setFont("Helvetica", 10)
            y -= 20
            for item in stock:
                c.drawString(30, y, f"Item ID: {item[0]}, Item Name: {item[1]}, Quantity: {item[2]}, Unit: {item[3]}, Price per Unit: {item[4]}, Total Cost: {item[2] * item[4]}")
                y -= 20

        # Add Company if not None
        if company is not None:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y, "Company:")
            c.setFont("Helvetica", 10)
            y -= 20
            if isinstance(company, dict):
                for key, value in company.items():
                    c.drawString(30, y, f"{key.capitalize()}: {value}")
                    y -= 20
            else:
                c.drawString(30, y, f"Company Info: {company}")  
                y -= 20

        c.save()

        return pdf_path
    except Exception as e:
        print(f"An error occurred while generating the PDF report: {e}")
        return None
eel.start("login.html", size=(1920, 1080))

