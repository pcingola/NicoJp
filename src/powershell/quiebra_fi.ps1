
$e = (Get-Content in.txt | Select-String -context 4 "exportador" | Get-Unique)
$e = $e -replace "`r`n","`t"
$e = $e -replace "> Exportador : ",""
$e = $e -replace "IBAN: ",""
$e = $e -replace "IBAN ",""
Out-File -InputObject $e -FilePath out.txt

$t = (Get-Content in.txt | Select-String "total lote")
$t = $t -replace "Total lote : ",""
$t = $t -replace "\.", ""
$t = $t -replace ",", "."
Out-File -Append -InputObject $t FilePath out.txt
