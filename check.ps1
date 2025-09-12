# Define the path to the Python scripts and output files
$pythonScript = "tesla_order_status.py"
$vinDecoderScript = "decode_vin.py"
$initialOutputFile = "initial_output.txt"
$currentOutputFile = "current_output.txt"
$vinOutputFile = "vin.txt"
$logFile = "script_log.txt"

# Function to log messages to file and console
function Write-Log {
    param (
        [string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    Add-Content -Path $logFile -Value $logMessage
}

# Function to check if the Python scripts exist
function Test-ScriptExists {
    if (-not (Test-Path $pythonScript)) {
        Write-Log "Python script '$pythonScript' not found in the current directory." -Level "ERROR"
        exit 1
    }
    if (-not (Test-Path $vinDecoderScript)) {
        Write-Log "Python script '$vinDecoderScript' not found in the current directory." -Level "ERROR"
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
            Write-Log "Change detected at line $($i + 1) since initial run:" -Level "INFO"
            if ($initialLine) { Write-Log "Initial: $initialLine" -Level "INFO" }
            if ($currentLine) { Write-Log "Current: $currentLine" -Level "INFO" }
        }
    }

    return $changesFound
}

# Function to extract VIN from output
function Get-VIN {
    param (
        [string]$output
    )

    # Look for a line containing "VIN:" followed by a 17-character VIN, handling ANSI color codes
    $vinPattern = "- VIN:.*?([A-HJ-NPR-Z0-9]{17})"
    $match = [regex]::Match($output, $vinPattern)
    if ($match.Success) {
        $vin = $match.Groups[1].Value
        Write-Log "Extracted VIN: $vin" -Level "INFO"
        return $vin
    }
    Write-Log "No valid VIN found in the output." -Level "WARNING"
    return $null
}

# Function to run the Python script, capture output, and decode VIN
function Invoke-PythonScript {
    try {
        Write-Log "Running $pythonScript at $(Get-Date)" -Level "INFO"
        $currentOutput = python $pythonScript 2>&1 | Out-String

        # Check for empty output
        if ([string]::IsNullOrWhiteSpace($currentOutput)) {
            Write-Log "Python script returned empty output." -Level "WARNING"
            return $false
        }

        # Log the raw output for debugging
        Write-Log "Raw output from $pythonScript :`n$currentOutput" -Level "DEBUG"

        # Extract VIN and decode it
        $vin = Get-VIN -output $currentOutput
        if ($vin) {
            Write-Log "Calling $vinDecoderScript with VIN: $vin" -Level "INFO"
            $vinOutput = python $vinDecoderScript $vin 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0) {
                Write-Log "VIN decoded successfully. Output written to $vinOutputFile." -Level "INFO"
                # Verify vin.txt exists
                if (Test-Path $vinOutputFile) {
                    $vinContent = Get-Content $vinOutputFile -Raw
                    Write-Log "Content of $vinOutputFile :`n$vinContent" -Level "DEBUG"
                } else {
                    Write-Log "$vinOutputFile was not created." -Level "ERROR"
                }
            } else {
                Write-Log "Failed to decode VIN: $vinOutput" -Level "ERROR"
            }
        } else {
            Write-Log "No valid VIN found in the output, skipping VIN decoding." -Level "WARNING"
        }

        # Check if initial output exists; if not, save current output as initial
        if (-not (Test-Path $initialOutputFile)) {
            Set-Content -Path $initialOutputFile -Value $currentOutput
            Write-Log "Initial output saved for future comparisons." -Level "INFO"
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
                Write-Log "No significant changes detected since initial run." -Level "INFO"
            }
        }

        # Save the current output
        Set-Content -Path $currentOutputFile -Value $currentOutput

        # Display the last run timestamp at the bottom
        Write-Log "Last run: $(Get-Date)" -Level "INFO"
        return $true
    }
    catch {
        Write-Log "Error running Python script: $_" -Level "ERROR"
        return $false
    }
}

# Main loop
try {
    # Verify scripts exist
    Test-ScriptExists

    # Run indefinitely until manually stopped (Ctrl+C)
    while ($true) {
        $success = Invoke-PythonScript
        if (-not $success) {
            Write-Log "Script execution failed or returned empty output. Retrying in 1 hour..." -Level "ERROR"
        }
        Write-Log "Waiting for 1 hour before next run... (Press Ctrl+C to stop)" -Level "INFO"
        Start-Sleep -Seconds 3600  # Sleep for 1 hour
    }
}
catch {
    Write-Log "An unexpected error occurred: $_" -Level "ERROR"
}
finally {
    Write-Log "Script stopped at $(Get-Date)" -Level "INFO"
}