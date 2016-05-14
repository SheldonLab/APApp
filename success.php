<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Success!</title>
    <link rel="stylesheet" href="style.css" media="screen">

</head>
<body>
<h2>Successfully Submitted!</h2>
<form method="post">
    <input type="submit" name="submit" value="Click here to go back">
</form>
</body>
</html>
<?php
if(isset($_POST['submit']) ) {
    header("Location: http://apapp.undo.it/client.php"); /* Redirect browser */
    exit();
}

?>