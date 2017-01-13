<?php
$array_content = scandir(".");
$actual_dir = getcwd() . "/";
$rm_dir = "/var/www/html";
$dir = str_replace($rm_dir, "", $actual_dir);
foreach ($array_content as &$content) {
  if ( ($content == "index.php") or preg_match("/\w*\.php/", $content) ){

  }
  elseif ( !scandir("./".$content) ){
    define_ex($dir,$content);
  }else{

    echo "<a href=".$dir.$content."/ >".$content."</a><br>";
  }
}

function define_ex($dir,$executable){
  $moves_file = "/var/www/html/back/moves.txt";
  $k = ".k";
  $executable_php = $executable.$k.".php";

  $write_php = "<?";
  $file = fopen($executable_php, "w");
  fwrite($file, $write_php);
  fclose($file);

  $write_php = "php \$file = fopen('".$moves_file."', 'a');" . PHP_EOL;
  $write_php .= "fwrite(\$file, '".$dir.$executable."\n');". PHP_EOL;
  $write_php .= "fclose(\$file);". PHP_EOL;
  $write_php .= "header('Location: ".$dir.$executable."');" . PHP_EOL;
  $write_php .= "?>";

  $file = fopen($executable_php, "a");
  fwrite($file, $write_php);
  fclose($file);
  echo "<a href=".$dir.$executable.$k.".php >".$executable."</a><br>";
}
?>
