
# Define input & output file names
# TODO: This should be just a command line argument

$inFile = "in.txt"
$outFile = "out.txt"

# Field numbers
# TODO: This should be in a configuration file?
$pageStart = 2
$pageEnd = 6

$montoUsdStart = 25
$montoUsdEnd = 42

$nameStart = 140
$nameEnd = 189

$paisStart = 602
$paisEnd = 604

$swiftStart = 700
$swiftEnd = 710

$cuentaStart = 850
$cuentaEnd = 865

#---
# Main
#---

# Read each line form input file
$dict = @{}
foreach($line in Get-Content $inFile) {
    if($line.Length -gt $cuentaEnd){
		# Parse lines
		$page = ($line[$pageStart..$pageEnd] -join '').Trim()
		$montoUsd = $line[$montoUsdStart..$montoUsdEnd] -join ''
		$name = $line[$nameStart..$nameEnd] -join ''
		$pais = $line[$paisStart..$paisEnd] -join ''
		$swift = $line[$swiftStart..$swiftEnd] -join ''
		$cuenta = $line[$cuentaStart..$cuentaEnd] -join ''

		# TODO: Write propper format checking for each field

		# Create output line
		$outLine = "`"$page`t$montoUsd`t$name`t$pais`t$swift`t$cuenta"

		# Add to dictionary to avoid repeated lines
		$dict[$page] = $outLine
    }
}

# Show unique lines (from dictionary) and write it to output file
$dict.values | ForEach-Object { Write-Output $_ } | Out-File -FilePath $outFile

