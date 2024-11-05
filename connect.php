<?php
// Database connection parameters
$servername = "localhost";
$username = "mayank.b.binjawadagi@gmail.com"; // Replace with your MySQL username
$password = "Bennettcreek123@"; // Replace with your MySQL password
$dbname = "jobs";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve form data
$title = $_POST['title'];
$description = $_POST['description'];
$salary = $_POST['salary'];
$location = $_POST['location'];

// Prepare and bind SQL statement
$sql = "INSERT INTO job_listings (title, description, salary, location) VALUES (?, ?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ssss", $title, $description, $salary, $location);

// Execute the statement
if ($stmt->execute()) {
    echo "New job added successfully.";
    echo "<br><a href='add_job.html'>Back to Add Job</a>"; // Link back to form
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

// Close connection
$stmt->close();
$conn->close();
?>
