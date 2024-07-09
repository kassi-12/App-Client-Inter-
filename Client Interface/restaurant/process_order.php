<?php
include 'functions.php';

header('Content-Type: application/json');

$data = json_decode(file_get_contents('php://input'), true);

if ($data) {
    $tableID = $data['tableID'];
    $userID = $data['userID'];
    $grossAmount = $data['grossAmount'];
    $sCharge = $data['sCharge'];
    $vat = $data['vat'];
    $discount = $data['discount'];
    $netAmount = $data['netAmount'];
    $orderItems = $data['orderItems'];

    $orderID = add_order($tableID, $userID, $grossAmount, $sCharge, $vat, $discount, $netAmount);

    if ($orderID) {
        $success = add_order_items($orderID, $orderItems);

        if ($success) {
            echo json_encode(['success' => true]);
        } else {
            echo json_encode(['success' => false, 'message' => 'Failed to add order items']);
        }
    } else {
        echo json_encode(['success' => false, 'message' => 'Failed to add order']);
    }
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid input data']);
}
?>
