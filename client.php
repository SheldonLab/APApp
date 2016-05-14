<!DOCTYPE HTML>
<html>
<head>
    <link rel="stylesheet" href="style.css" media="screen">
    <style>
        .error {color: #FF0000;}
    </style>
</head>
<body>

<?php
// define variables and set to empty values
$nameErr = $emailErr = $genderErr = $Err = "";
$name  = $gender = $comment = $exam_number = "";
$number = 0;
$tablea = $tableb = $time = $table = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (empty($_POST["initials"])) {
        $nameErr = "Initials are required";
        $Err = "Not Submitted";
    } else {
        $name = test_input($_POST["initials"]);
        // check if name only contains letters and whitespace
        if (!preg_match("/^[a-zA-Z]*$/", $name)) {
            $nameErr = "Only letters are allowed";
            $Err = "Not Submitted";
            $name = '';
        }
    }

    if (empty($_POST["number"])) {
        $numberErr = "Number is required";
        $Err = "Not Submitted";
    } else {
        $number = test_input($_POST["number"]);
        // check if number is a number
        if (!preg_match("/^[0-9]*$/", $number)) {
            $numberErr = "Only numbers are allowed";
            $Err = "Not Submitted";
        }
    }
    if (empty($_POST["exam_number"])) {
        $numberErr = "Number is required";
        $Err = "Not Submitted";
    } else {
        $exam_number = test_input($_POST["number"]);
        // check if number is a number
        if (!preg_match("/^[0-9]*$/", $number)) {
            $numberErr = "Only numbers are allowed";
            $Err = "Not Submitted";
        }
    }
}


function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

if(isset($_POST['submit']) )
{
    $tablea = $_POST['tablea'];
    $tableb = $_POST['tableb'];
    $table = $tablea . "-" . $tableb;
    $time = $_POST['time'];

    if (( $tablea === "") || ( $tableb === "") || ( $time === "")){
        $Err = "Not Submitted";
    }
}
?>

<h2>AP Physics submission form</h2>
<p><span class="error">* required field.</span></p>
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">

    <p>
    <div class="form-row">
        <div class="left">
        <p>
            Exam Number
            <select name="tablea">
                <option value="">Select...</option>
                <option value="80">80</option>
                <option value="82">82</option>
                <option value="83">83</option>
                <option value="84">84</option>
            </select>
        </p>
        </div>
        <div class="right">
        <p>
            Form
            <select name="tableb">
                <option value="">Select...</option>
                <option value="O">O</option>
                <option value="A">A</option>
                <option value="I">I</option>
                <option value="Z">Z</option>
                <option value="Other">Other</option>
            </select>
        </p>
        </div>

        <div class="left">
            Question Number: <input type="number" name="exam_number" value="">
            <span class="error">* <?php echo $numberErr;?></span>

            <p>
                Session
                <select name="time">
                    <option value="">Select...</option>
                    <option value="AM1">AM1</option>
                    <option value="AM2">AM2</option>
                    <option value="PM1">PM1</option>
                    <option value="PM2">PM2</option>
                </select>
            </p>
            <br><br>
            Leader Name: <input type="text" name="initials" value="">
            <span class="error">* <?php echo $nameErr;?></span>
            <br><br>

            Total for Session: <input type="number" name="number" value="">
            <span class="error">* <?php echo $numberErr;?></span>
            <br><br>




            <input type="submit" name="submit" value="Submit">
        </div>


    </div>
    </p>
</form>



<?php
if(isset($_POST['submit']) ) {
    if ($Err == "" and ($tablea != "")) {
        $Err = "Submitted!";
    } else {
        header("Location: http://apapp.undo.it/fail.php"); /* Redirect browser */
        exit();
    }

    if ($Err === "Submitted!") {
        $arr = array('item2' => $time, 'item1' => $table, 'number' => $number, 'initials' => $name);
        $json = json_encode($arr);
        $uri = "http://172.31.55.173:8000/data";
        $curl = curl_init($uri);
        curl_setopt($curl, CURLOPT_HTTPHEADER,
            array("Content-type: application/json"));
        curl_setopt($curl, CURLOPT_POST, true);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $json);
        $response = curl_exec($curl);
        curl_close($curl);
        header("Location: http://apapp.undo.it/success.php"); /* Redirect browser */
        exit();
    }
}
?>

</body>
</html>