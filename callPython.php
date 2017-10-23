<?php
  $prime = "apple";
  $cmd = "python sample.py --prime $prime";
  $python =  exec($cmd);

  echo "임의 단어 : " . $prime . "<br>";
  echo "실행 명령어 : " . $cmd . "<br>"; 
  echo "출력 결과 : " . $python . "<br>";
?>
