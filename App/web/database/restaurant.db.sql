BEGIN;

CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    language VARCHAR(255),
    theme VARCHAR(255),
    restaurant_name VARCHAR(255),
    address TEXT,
    phone VARCHAR(255),
    currency VARCHAR(255),
    timezone VARCHAR(255),
    tax_rate INT
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_id INT NOT NULL,
    user_id INT NOT NULL,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    gross_amount INT NOT NULL,
    s_charge INT NOT NULL,
    vat INT NOT NULL,
    discount INT DEFAULT 0,
    method VARCHAR(255),
    status VARCHAR(255) NOT NULL,
    net_amount INT NOT NULL
);

CREATE TABLE IF NOT EXISTS tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(255),
    capacity INT,
    availability VARCHAR(255),
    status VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    gender VARCHAR(255),
    phone VARCHAR(255),
    bio TEXT,
    group_id INT,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE IF NOT EXISTS groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    unit VARCHAR(255),
    price_per_unit INT
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category_id INT NOT NULL,
    price INT NOT NULL,
    description TEXT,
    status VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert initial data
INSERT INTO category (id, name, status) VALUES 
(1, 'F1', 'active'),
(2, 'F2', 'active'),
(3, 'F3', 'active');

INSERT INTO orders (id, table_id, user_id, order_time, gross_amount, s_charge, vat, discount, method, status, net_amount) VALUES 
(1, 1, 1, '2024-07-01 16:22:21', 48.0, 1.44, 6.24, 0.0, 'Cheque', 'Paid', 55.68),
(2, 1, 1, '2024-07-01 19:32:04', 3.0, 0.09, 0.39, 0.0, 'Cheque', 'Paid', 3.48);

INSERT INTO tables (id, table_name, capacity, availability, status) VALUES 
(1, 'T1', 2, 'available', 'active'),
(2, 'T2', 5, 'available', 'active'),
(3, 'T3', 4, 'available', 'active');

INSERT INTO users (id, username, email, password, first_name, last_name, gender, phone, bio, group_id) VALUES 
(1, 'Kassimi', 'kassimi@ease.de', '1234', 'kassimi', 'abderrahmane', 'male', '0607553567', 'kassimi admin', 1),
(2, 'sabi', 'sabi@ease.de', '1234', 'sabi', 'houssam', 'male', '0600000000', 'sabi', 1),
(3, 'ziyad', 'bg@ease.de', '1234', 'ziyad', 'bg', 'male', '0600000000', 'ziyad', 1);

INSERT INTO groups (id, group_name) VALUES 
(1, 'Admin'),
(2, 'Server'),
(3, 'Kitchen Staff'),
(4, 'host/hostess'),
(5, 'Manager'),
(6, 'Bartender'),
(7, 'Waiter'),
(8, 'Chef'),
(9, 'Cashier');

INSERT INTO stock (id, item_name, quantity, unit, price_per_unit) VALUES 
(5, 'Milke', 1, 'liter', 5.0);

INSERT INTO products (id, name, category_id, price, description, status) VALUES 
(2, 'TACOS', 1, 3.0, 'tt', 'active');

COMMIT;
