
# Define input & output file names
# TODO: This should be just a command line argument

$inFile = "in.txt"
$outFile = "out.txt"

# Field numbers
$nameField = 1
$currencyField = 3
$amountField = 4
$countryField = 5
$bankField = 6
$ibanField = 7
$swiftField = 8
$abaField = 9
$accountField = 10

#---
# Main
#---

# Read each line form input file
$dict = @{}
foreach($line in Get-Content $inFile) {
	$fields = $line.Split("`t")
    if($fields.Length -gt $accountField){
		# Parse lines
		$name = $field[nameField].Trim()
		$currency = $field[currencyField].Trim()
		$amount = $field[amountField].Trim()
		$country = $field[countryField].Trim()
		$bank = $field[bankField].Trim()
		$iban = $field[ibanField].Trim()
		$swift = $field[swiftField].Trim()
		$aba = $field[abaField].Trim()
		$account = $field[accountField].Trim()

		# Prepend '/'
		$account = "/$account"

		# Create output line
		$outLine = "`"$name`t4$currency`t$amount`t$country`t$bank`t$iban`t$swift`t$aba`t$account"

		# Add to dictionary to avoid repeated lines
		$dict[$name] = $outLine
    }
}

# Show unique lines (from dictionary) and write it to output file
$dict.values | ForEach-Object { Write-Output $_ } | Out-File -FilePath $outFile

