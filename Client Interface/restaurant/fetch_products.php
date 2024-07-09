<?php
include 'functions.php';

header('Content-Type: application/json');
$products = fetch_products();
if ($products === null) {
    echo json_encode([]);
} else {
    echo json_encode($products);
}
?>
