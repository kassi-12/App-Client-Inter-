
function customAlert(message) {
    const appName = "Ease Dine"; // Replace with your application's name
    const fullMessage = `${appName} says\n\n${message}`;
    alert(fullMessage);
}
const ctx = document.getElementById('ordersChart').getContext('2d');

async function fetchOrders() {
    try {
        const orders = await eel.fetch_orders_paid()();
        console.log('Fetched orders:', orders);  // Log fetched orders
        return orders;
    } catch (error) {
        console.error('Error fetching orders:', error);
        return [];
    }
}

function updateChart(orders) {
    const currentYear = 2024;
    const monthlyAmounts = Array(12).fill(0);

    orders.forEach(order => {
        const orderDate = new Date(order[0]);  // Accessing order_time as the first element
        const orderYear = orderDate.getFullYear();

        if (orderYear === currentYear) {
            const month = orderDate.getMonth();
            monthlyAmounts[month] += order[1];  // Accessing net_amount as the second element
        }
    });

    const data = {
        labels: [
            'January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December'
        ],
        datasets: [{
            label: 'Total Paid Orders',
            data: monthlyAmounts,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    new Chart(ctx, config);
}

function updateTable(orders) {
    const currentYear = 2024;
    const tbody = document.querySelector('table tbody');
    tbody.innerHTML = '';

    const monthlyAmounts = Array(12).fill(0);

    orders.forEach(order => {
        const orderDate = new Date(order[0]);  // Accessing order_time as the first element
        const orderYear = orderDate.getFullYear();

        if (orderYear === currentYear) {
            const month = orderDate.getMonth();
            monthlyAmounts[month] += order[1];  // Accessing net_amount as the second element
        }
    });

    monthlyAmounts.forEach((amount, index) => {
        const row = document.createElement('tr');
        const monthYearCell = document.createElement('td');
        const amountCell = document.createElement('td');

        monthYearCell.textContent = `${currentYear}-${String(index + 1).padStart(2, '0')}`;
        amountCell.textContent = `$${amount.toFixed(2)}`;

        row.appendChild(monthYearCell);
        row.appendChild(amountCell);
        tbody.appendChild(row);
    });

    const tfoot = document.querySelector('table tfoot th:last-child');
    const totalAmount = monthlyAmounts.reduce((sum, amount) => sum + amount, 0);
    tfoot.textContent = `$${totalAmount.toFixed(2)}`;
}

async function init() {
    const orders = await fetchOrders();
    updateChart(orders);
    updateTable(orders);
}

init();
async function saveReport() {
    try {
        const users = await eel.fetch_users()();
        const groups = await eel.fetch_groups()();
        const categories = await eel.fetch_categorys()();
        const products = await eel.fetch_products()();
        const tables = await eel.fetch_tables()();
        const stock = await eel.fetch_stock()();
        const company = await eel.fetch_company_settings()();
        const ord = await eel.fetch_orders_pdf()();
        const pdfPath = await eel.generate_pdf_report(
            ord, users, groups, categories, products, tables, stock, company
        )();

        if (pdfPath) {
            console.log('PDF saved successfully at:', pdfPath);
            alert('Report saved successfully!');
        } else {
            console.error('Error saving report: PDF path is empty');
            alert('Failed to save report. Please try again.');
        }
    } catch (error) {
        console.error('Error saving report:', error);
        alert('An error occurred while saving the report. Please try again.');
    }
}

