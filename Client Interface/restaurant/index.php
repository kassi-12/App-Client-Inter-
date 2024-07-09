<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Sharp" rel="stylesheet">
    <link rel="stylesheet" href="./mang_style.css">
    <link rel="stylesheet" href="./style.css">
    <link rel="stylesheet" href="./add_style.css">
    <title>Ease Dine</title>
    <link rel="icon" href="./logo.ico">
    
</head>
<body>
<main>
    <!-- The Modal -->
        <div id="menuModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <img src="Black Orange Modern Restaurant Food Menu.png" alt="Restaurant Menu" class="menu-img">
            </div>
        </div>

        <div class="manage-users-container">
        <div class="button-container">
        <button type="button" id="view-menu-btn" class="submit-btn">View Menu</button>
                    
        </div>
            <form id="order-form" action="process_order.php" method="POST">
                <div class="form-group">
                    <label for="table">Table</label>
                    <select id="table" name="table" class="form-control">
                        <!-- PHP code for table options -->
                    </select>
                </div>
                <div id="product-container">
                    <div class="form-group">
                        <label for="product">Product</label>
                        <span class="material-icons-sharp add-product-btn">add</span>
                    </div>
                </div>
                <div id="order-list">
                    <!-- Dynamically added products will appear here -->
                </div>
                <div class="totals">
                    <div class="form-group">
                        <label for="gross-amount">Gross Amount</label>
                        <input type="text" id="gross-amount" name="gross-amount" class="form-control" readonly>
                    </div>
                    <div class="form-group">
                        <label for="s-charge">S-Charge 3%</label>
                        <input type="text" id="s-charge" name="s-charge" class="form-control" readonly>
                    </div>
                    <div class="form-group">
                        <label for="vat">VAT 13%</label>
                        <input type="text" id="vat" name="vat" class="form-control" readonly>
                    </div>
                    <div class="form-group">
                        <label for="discount">Discount</label>
                        <input type="text" id="discount" name="discount" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="net-amount">Net Amount</label>
                        <input type="text" id="net-amount" name="net-amount" class="form-control" readonly>
                    </div>
                </div>
                <div class="button-container">
                    <button type="submit" id="create-order-btn" class="submit-btn">Create Order</button>
                    
                </div>
            </form>
        </div>
    </main>

    
    <!-- The Modal -->
    <div id="menuModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <img src="Black Orange Modern Restaurant Food Menu.png" alt="Restaurant Menu" style="width:100%;">
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            populateTableSelect();
            populateProductSelect();

            document.querySelector('.add-product-btn').addEventListener('click', addProductRow);
            document.getElementById('order-form').addEventListener('submit', createOrder);

            async function populateTableSelect() {
                try {
                    const response = await fetch('fetch_tables.php'); 
                    if (!response.ok) throw new Error("Failed to fetch tables");
                    const tables = await response.json();
                    const tableSelect = document.getElementById('table');
                    tableSelect.innerHTML = ''; 

                    tables.forEach(table => {
                        if (table.availability === 'available' && table.status === 'active') {
                            const option = document.createElement('option');
                            option.value = table.id;
                            option.textContent = table.table_name;
                            tableSelect.appendChild(option);
                        }
                    });

                    console.log("Tables populated successfully!");
                } catch (error) {
                    console.error("Error fetching tables:", error);
                }
            }

            async function populateProductSelect(container = null) {
                try {
                    const response = await fetch('fetch_products.php'); 
                    if (!response.ok) throw new Error("Failed to fetch products");
                    const products = await response.json();
                    const productContainers = container ? [container] : document.querySelectorAll('#product-container .form-group');

                    productContainers.forEach(container => {
                        const productSelect = container.querySelector('select[name="product[]"]');
                        const priceInput = container.querySelector('input[name="price[]"]');
                        const quantityInput = container.querySelector('input[name="quantity[]"]');

                        if (productSelect) {
                            productSelect.innerHTML = '<option value="">Select a product</option>';

                            products.forEach(product => {
                                if (product.status === 'active') {
                                    const option = document.createElement('option');
                                    option.value = product.id;
                                    option.textContent = product.name;
                                    option.dataset.price = product.price; 
                                    productSelect.appendChild(option);
                                }
                            });

                            productSelect.addEventListener('change', (event) => {
                                const selectedOption = event.target.selectedOptions[0];
                                const price = parseFloat(selectedOption ? selectedOption.dataset.price : '');
                                priceInput.value = isNaN(price) ? '' : price.toFixed(2);
                                calculateTotals();
                            });

                            priceInput.value = ''; 
                            if (quantityInput) {
                                quantityInput.value = '1'; 
                            }
                        } else {
                            console.error("Product select element not found within the container:", container);
                        }
                    });

                    console.log("Products populated successfully!");
                } catch (error) {
                    console.error("Error fetching products:", error);
                }
            }

            function addProductRow() {
                const productContainer = document.getElementById('product-container');
                const newProductRow = document.createElement('div');
                newProductRow.classList.add('form-group');
                newProductRow.innerHTML = `
                    <select name="product[]" class="form-control">
                        <!-- Options will be populated dynamically -->
                    </select>
                    <input type="text" name="price[]" class="form-control" readonly>
                    <input type="number" name="quantity[]" class="form-control" min="1" value="1">
                    <span class="material-icons-sharp remove-product-btn">remove</span>
                `;

                productContainer.appendChild(newProductRow);

                newProductRow.querySelector('.remove-product-btn').addEventListener('click', () => {
                    productContainer.removeChild(newProductRow);
                    calculateTotals();
                });

                populateProductSelect(newProductRow);

                const quantityInput = newProductRow.querySelector('input[name="quantity[]"]');
                if (quantityInput) {
                    quantityInput.addEventListener('input', calculateTotals);
                }

                calculateTotals();
            }

            function calculateTotals() {
                const productContainers = document.querySelectorAll('#product-container .form-group');
                let grossAmount = 0;

                productContainers.forEach(container => {
                    const priceInput = container.querySelector('input[name="price[]"]');
                    const quantityInput = container.querySelector('input[name="quantity[]"]');
                    const price = parseFloat(priceInput ? priceInput.value : 0) || 0;
                    const quantity = parseInt(quantityInput ? quantityInput.value : 0) || 0;
                    grossAmount += price * quantity;
                });

                const sCharge = grossAmount * 0.03;
                const vat = grossAmount * 0.13;
                const discount = parseFloat(document.getElementById('discount').value) || 0;
                const netAmount = grossAmount + sCharge + vat - discount;

                document.getElementById('gross-amount').value = grossAmount.toFixed(2);
                document.getElementById('s-charge').value = sCharge.toFixed(2);
                document.getElementById('vat').value = vat.toFixed(2);
                document.getElementById('net-amount').value = netAmount.toFixed(2);
            }

            document.getElementById('discount').addEventListener('input', calculateTotals);

            
            async function createOrder(event) {
                event.preventDefault();

                const tableId = document.getElementById('table').value;
                const userId = 1; 
                const grossAmount = parseFloat(document.getElementById('gross-amount').value);
                const sCharge = parseFloat(document.getElementById('s-charge').value);
                const vat = parseFloat(document.getElementById('vat').value);
                const discount = parseFloat(document.getElementById('discount').value);
                const netAmount = parseFloat(document.getElementById('net-amount').value);

                const orderItems = [];
                const productContainers = document.querySelectorAll('#product-container .form-group');
                productContainers.forEach(container => {
                    const productSelect = container.querySelector('select[name="product[]"]');
                    const priceInput = container.querySelector('input[name="price[]"]');
                    const quantityInput = container.querySelector('input[name="quantity[]"]');
                    const productId = parseInt(productSelect ? productSelect.value : 0);
                    const price = parseFloat(priceInput ? priceInput.value : 0);
                    const quantity = parseInt(quantityInput ? quantityInput.value : 0);

                    if (!isNaN(productId) && !isNaN(price) && !isNaN(quantity)) {
                        orderItems.push({
                            productID: productId,
                            quantity: quantity,
                            price: price.toFixed(2)
                        });
                    }
                });

                const orderData = {
                    tableID: tableId,
                    userID: userId,
                    grossAmount: grossAmount.toFixed(2),
                    sCharge: sCharge.toFixed(2),
                    vat: vat.toFixed(2),
                    discount: discount.toFixed(2),
                    netAmount: netAmount.toFixed(2),
                    orderItems: orderItems
                };

                try {
                    const response = await fetch('process_order.php', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(orderData)
                    });

                    const resultText = await response.text(); 
                    let result;

                    try {
                        result = JSON.parse(resultText); 
                    } catch (e) {
                        console.error("Failed to parse JSON:", resultText);
                        throw new Error("Invalid JSON response");
                    }

                    if (result.success) {
                        console.log("Order created successfully!");

                        // Generate order details text
                        const orderDetails = generateOrderDetailsText(orderData);
                        // Trigger download
                        downloadOrderDetails(orderDetails, `Order_${result.orderID}.txt`);

                        alert("Order created successfully!");
                    } else {
                        console.error("Failed to create order:", result.message);
                        alert("Failed to create order. Please try again."); 
                    }
                } catch (error) {
                    console.error("Error creating order:", error);
                    alert("Error creating order. Please try again later."); 
                }
            }

            function generateOrderDetailsText(orderData) {
                let orderDetails = `Table: ${document.getElementById('table').selectedOptions[0].textContent}\n`;
                orderDetails += `Gross Amount: ${orderData.grossAmount}\n`;
                orderDetails += `S-Charge: ${orderData.sCharge}\n`;
                orderDetails += `VAT: ${orderData.vat}\n`;
                orderDetails += `Discount: ${orderData.discount}\n`;
                orderDetails += `Net Amount: ${orderData.netAmount}\n\n`;
                orderDetails += `Order Items:\n`;

                orderData.orderItems.forEach(item => {
                    const productSelect = document.querySelector(`select[name="product[]"] option[value="${item.productID}"]`);
                    if (productSelect) {
                        const productName = productSelect.textContent;
                        orderDetails += `- Product: ${productName}, Quantity: ${item.quantity}, Price: ${item.price}\n`;
                    } else {
                        console.error(`Product select element not found for product ID: ${item.productID}`);
                    }
                });

                return orderDetails;
            }

            function downloadOrderDetails(orderDetails, fileName) {
                const blob = new Blob([orderDetails], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = fileName;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }
        });

        // Modal JavaScript
        var modal = document.getElementById("menuModal");
        var btn = document.getElementById("view-menu-btn");
        var span = document.getElementsByClassName("close")[0];

        btn.onclick = function() {
            modal.style.display = "block";
        }

        span.onclick = function() {
            modal.style.display = "none";
        }

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    </script>
</body>
</html>
