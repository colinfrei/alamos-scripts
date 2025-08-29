@echo off
setlocal

REM ================================
REM Konfigurierbare Werte
set "orgId=755"
set "authKey=r0liuU2yk8R6gGcXgd1ZgXFZylX43kSe"
REM ================================

if "%~1"=="" (
    echo Usage: mokos_transform_json.bat "{json_input}"
    exit /b 1
)

REM Combine all arguments into one JSON string
set "jsonInput=%*"

REM Call PowerShell with JSON as argument
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$inputJson = '%jsonInput%'; " ^
    "$orgId = '%orgId%'; " ^
    "$authKey = '%authKey%'; " ^
    "$data = $inputJson | ConvertFrom-Json; " ^
    "$output = @{ " ^
    "    type = 'ALARM'; " ^
    "    timestamp = $data.AlarmStart; " ^
    "    sender = 'KNZ'; " ^
    "    authorization = $authKey; " ^
    "    data = @{ " ^
    "        externalId = $data.AlarmId; " ^
    "        keyword = $data.AlertType; " ^
    "        keyword_description = ''; " ^
    "        keyword_misc = ''; " ^
    "        location = @{ " ^
    "            coordinate = @($data.Coordinate | Where-Object { $_.System -eq 'WGS84' } | ForEach-Object { $_.North; $_.East }); " ^
    "            building = ''; building_id = ''; crossing = ''; " ^
    "            street = $data.Street; house = $data.StreetNr; additional = ''; " ^
    "            postalCode = $data.ZipCode; city = $data.City; city_abbr = '' " ^
    "        }; " ^
    "        caller = @{ name = ''; contact = $data.Caller }; " ^
    "        custom = @{ remark = '' } " ^
    "    } " ^
    "}; " ^
    "$groupsDict = @{ " ^
    "    'alarmgruppe_atemschutz' = $false; " ^
    "    'alarmgruppe_gruppe1' = $false; " ^
    "    'alarmgruppe_gruppe2' = $false; " ^
    "    'alarmgruppe_gruppe3' = $false; " ^
    "    'alarmgruppe_gruppe4' = $false; " ^
    "    'alarmgruppe_hrf' = $false; " ^
    "    'alarmgruppe_kommandogruppe' = $false; " ^
    "    'alarmgruppe_konferenzgespraech' = $false; " ^
    "    'alarmgruppe_notfalltreffpunkte' = $false; " ^
    "    'alarmgruppe_strassenrettung' = $false; " ^
    "    'alarmgruppe_verkehrsgruppe' = $false " ^
    "}; " ^
    "$mapping = @{ " ^
    "    '4'   = 'alarmgruppe_atemschutz'; " ^
    "    '1'   = 'alarmgruppe_gruppe1'; " ^
    "    '2'   = 'alarmgruppe_gruppe2'; " ^
    "    '50'  = 'alarmgruppe_gruppe3'; " ^
    "    '111' = 'alarmgruppe_gruppe4'; " ^
    "    '200' = 'alarmgruppe_hrf'; " ^
    "    '3'   = 'alarmgruppe_kommandogruppe'; " ^
    "    '6'   = 'alarmgruppe_konferenzgespraech'; " ^
    "    '468' = 'alarmgruppe_notfalltreffpunkte'; " ^
    "    '53'  = 'alarmgruppe_strassenrettung'; " ^
    "    '5'   = 'alarmgruppe_verkehrsgruppe'; " ^
    "}; " ^
    "$org = $data.Organisations | Where-Object { $_.Id -eq $orgId }; " ^
    "if ($org -and $org.Groups) { " ^
    "    foreach ($g in $org.Groups) { " ^
    "        $id = $g.Id.ToString(); " ^
    "        if ($mapping.ContainsKey($id)) { $groupsDict[$mapping[$id]] = $true } else { Write-Host 'Unknown group id:' $id '('$g.Name')' }" ^
    "    } " ^
    "} " ^
    "foreach ($k in $groupsDict.Keys) { $output.data.custom[$k] = $groupsDict[$k] } " ^
    "$jsonOut = $output | ConvertTo-Json -Depth 10 -Compress; " ^
    "Invoke-RestMethod -Uri 'http://127.0.0.1:83/rest/external/http/alarm/v2' -Method POST -Body $jsonOut -ContentType 'application/json'"

endlocal
