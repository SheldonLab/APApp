<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" media="screen">
    <meta charset="UTF-8">
    <title>Failed1</title>

</head>
<body>
<h2>Failed to Submit!</h2>
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