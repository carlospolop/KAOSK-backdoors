<?php

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017, Carlos Polop Martin <carlospolop[at]gmail.com
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted
# provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and
# the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions
# and the following disclaimer in the documentation and/or other materials provided with the
# distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


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
