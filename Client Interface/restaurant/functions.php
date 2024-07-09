<?php
$db_path = 'C:/Users/KASSIMI/Documents/RMS/web/database/restaurant.db';

function fetch_products() {
    global $db_path;
    try {
        $conn = new SQLite3($db_path);
        $results = $conn->query('SELECT id, name, category_id, price, status, description FROM products');
        $products = [];
        while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
            $products[] = $row;
        }
        $conn->close();
        return $products;
    } catch (Exception $e) {
        error_log("An error occurred while fetching products: " . $e->getMessage());
        return [];
    }
}

function fetch_tables() {
    global $db_path;
    try {
        $conn = new SQLite3($db_path);
        $results = $conn->query('SELECT id, table_name, capacity, availability, status FROM tables');
        $tables = [];
        while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
            $tables[] = $row;
        }
        $conn->close();
        return $tables;
    } catch (Exception $e) {
        error_log("An error occurred while fetching tables: " . $e->getMessage());
        return [];
    }
}

function add_order($table_id, $user_id, $gross_amount, $s_charge, $vat, $discount, $net_amount) {
    global $db_path;
    try {
        $conn = new SQLite3($db_path);
        $stmt = $conn->prepare('INSERT INTO orders (table_id, user_id, gross_amount, s_charge, vat, discount, net_amount, status) VALUES (?, ?, ?, ?, ?, ?, ?, "In Progress")');
        $stmt->bindValue(1, $table_id, SQLITE3_INTEGER);
        $stmt->bindValue(2, $user_id, SQLITE3_INTEGER);
        $stmt->bindValue(3, $gross_amount, SQLITE3_FLOAT);
        $stmt->bindValue(4, $s_charge, SQLITE3_FLOAT);
        $stmt->bindValue(5, $vat, SQLITE3_FLOAT);
        $stmt->bindValue(6, $discount, SQLITE3_FLOAT);
        $stmt->bindValue(7, $net_amount, SQLITE3_FLOAT);
        $stmt->execute();
        $order_id = $conn->lastInsertRowID();
        $conn->close();
        return $order_id;
    } catch (Exception $e) {
        error_log("An error occurred while adding order: " . $e->getMessage());
        return null;
    }
}

function add_order_items($order_id, $order_items) {
    global $db_path;
    try {
        $conn = new SQLite3($db_path);
        $conn->exec('BEGIN');
        $stmt = $conn->prepare('INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)');
        foreach ($order_items as $item) {
            $stmt->bindValue(1, $order_id, SQLITE3_INTEGER);
            $stmt->bindValue(2, $item['productID'], SQLITE3_INTEGER);
            $stmt->bindValue(3, $item['quantity'], SQLITE3_INTEGER);
            $stmt->bindValue(4, $item['price'], SQLITE3_FLOAT);
            $stmt->execute();
        }
        $conn->exec('COMMIT');
        $conn->close();
        return true;
    } catch (Exception $e) {
        $conn->exec('ROLLBACK');
        error_log("An error occurred while adding order items: " . $e->getMessage());
        return false;
    }
}
?>
