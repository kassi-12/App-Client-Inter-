<?php
include 'functions.php';

header('Content-Type: application/json');
$tables = fetch_tables();
if ($tables === null) {
    echo json_encode([]);
} else {
    echo json_encode($tables);
}
?>
