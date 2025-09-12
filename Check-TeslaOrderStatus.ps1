# Script to run python tesla_order_status.py every hour, track output changes since first run, highlight differences, and display only the latest output with timestamp

# Define the path to the Python script and output files
$pythonScript = "tesla_order_status.py"
$initialOutputFile = "initial_output.txt"
$currentOutputFile = "current_output.txt"

# Function to check if the Python script exists
function Test-ScriptExists {
    if (-not (Test-Path $pythonScript)) {
        Write-Error "Python script '$pythonScript' not found in the current directory."
        exit 1
    }
}

# Function to normalize output to reduce false positives
function Normalize-Output {
    param (
        [string]$output
    )

    # Remove extra whitespace, newlines, and common timestamp patterns
    $normalized = $output -replace '\s+', ' ' # Collapse multiple spaces
    $normalized = $normalized -replace '^\s+|\s+$', '' # Trim leading/trailing spaces
    $normalized = $normalized -replace '\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:\s*[+-]\d{2}:\d{2})?', '' # Remove ISO timestamps
    $normalized = $normalized -replace '\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}(?:\s*[AP]M)?', '' # Remove MM/DD/YYYY timestamps
    return $normalized.Trim()
}

# Function to compare outputs and highlight differences
function Compare-Outputs {
    param (
        [string]$currentOutput,
        [string]$initialOutput
    )

    # Split outputs into lines for comparison
    $currentLines = $currentOutput -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ }
    $initialLines = $initialOutput -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ }

    # Compare line by line
    $maxLines = [Math]::Max($currentLines.Length, $initialLines.Length)
    $changesFound = $false

    for ($i = 0; $i -lt $maxLines; $i++) {
        $currentLine = if ($i -lt $currentLines.Length) { $currentLines[$i] } else { "" }
        $initialLine = if ($i -lt $initialLines.Length) { $initialLines[$i] } else { "" }

        # Normalize lines before comparison
        $normalizedCurrent = Normalize-Output -output $currentLine
        $normalizedInitial = Normalize-Output -output $initialLine

        if ($normalizedCurrent -ne $normalizedInitial) {
            $changesFound = $true
            Write-Host "Change detected at line $($i + 1) since initial run:" -ForegroundColor Yellow
            if ($initialLine) { Write-Host "Initial: $initialLine" -ForegroundColor Red }
            if ($currentLine) { Write-Host "Current: $currentLine" -ForegroundColor Green }
        }
    }

    return $changesFound
}

# Function to run the Python script and capture output
function Invoke-PythonScript {
    try {
        Write-Host "Running $pythonScript at $(Get-Date)" -ForegroundColor Cyan
        $currentOutput = python $pythonScript 2>&1 | Out-String

        # Check for empty output
        if ([string]::IsNullOrWhiteSpace($currentOutput)) {
            Write-Warning "Python script returned empty output."
            return $false
        }

        # Check if initial output exists; if not, save current output as initial
        if (-not (Test-Path $initialOutputFile)) {
            Set-Content -Path $initialOutputFile -Value $currentOutput
            Write-Host "Initial output saved for future comparisons."
        }

        # Read the initial output
        $initialOutput = if (Test-Path $initialOutputFile) { Get-Content $initialOutputFile -Raw } else { "" }

        # Clear the console to show only the latest output
        Clear-Host
        Write-Host $currentOutput

        # Compare with initial output and highlight changes
        if ($initialOutput) {
            $changes = Compare-Outputs -currentOutput $currentOutput -initialOutput $initialOutput
            if (-not $changes) {
                Write-Host "No significant changes detected since initial run." -ForegroundColor Gray
            }
        }

        # Save the current output
        Set-Content -Path $currentOutputFile -Value $currentOutput

        # Display the last run timestamp at the bottom
        Write-Host "`nLast run: $(Get-Date)" -ForegroundColor Cyan
        return $true
    }
    catch {
        Write-Error "Error running Python script: $_"
        return $false
    }
}

# Main loop
try {
    # Verify script exists
    Test-ScriptExists

    # Run indefinitely until manually stopped (Ctrl+C)
    while ($true) {
        $success = Invoke-PythonScript
        if (-not $success) {
            Write-Host "Script execution failed or returned empty output. Retrying in 1 hour..." -ForegroundColor Red
        }
        Write-Host "Waiting for 1 hour before next run... (Press Ctrl+C to stop)" -ForegroundColor Cyan
        Start-Sleep -Seconds 3600  # Sleep for 1 hour
    }
}
catch {
    Write-Error "An unexpected error occurred: $_"
}
finally {
    Write-Host "Script stopped at $(Get-Date)" -ForegroundColor Cyan
}
