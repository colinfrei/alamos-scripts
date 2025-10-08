@echo off
setlocal

REM ================================
REM Configurable values
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
    "        message = @($data.ObjectName); " ^
    "        location = @{ " ^
    "            coordinate = @($data.Coordinate | Where-Object { $_.System -eq 'WGS84' } | ForEach-Object { $_.East; $_.North }); " ^
    "            building = ''; " ^
    "            building_id = ''; " ^
    "            crossing = ''; " ^
    "            street = $data.Street; " ^
    "            house = $data.StreetNr; " ^
    "            additional = ''; " ^
    "            postalCode = $data.ZipCode; " ^
    "            city = $data.City; " ^
    "            city_abbr = '' " ^
    "        }; " ^
    "        caller = @{ name = ''; contact = $data.Caller }; " ^
    "        custom = @{ " ^
    "            pagerText = $data.PagerText; " ^
    "            lv95_east = ($data.Coordinate | Where-Object { $_.System -eq 'LV95' } | Select-Object -ExpandProperty East); " ^
    "            lv95_north = ($data.Coordinate | Where-Object { $_.System -eq 'LV95' } | Select-Object -ExpandProperty North); " ^
    "            alarmGroups = ''; " ^
    "            alarmGroupsOther = '' " ^
    "        } " ^
    "    } " ^
    "}; " ^
    "$org = $data.Organisations | Where-Object { $_.Id -eq $orgId }; " ^
    "if ($org -and $org.Groups) { " ^
    "    $groupNames = @(); " ^
    "    foreach ($g in $org.Groups) { $groupNames += $g.Name } " ^
    "    if ($groupNames) { $output.data.custom.alarmGroups = ($groupNames -join \"`n\") } " ^
    "} " ^
    "$otherOrgGroups = @(); " ^
    "$otherOrgs = $data.Organisations | Where-Object { $_.Id -ne $orgId }; " ^
    "foreach ($o in $otherOrgs) { " ^
    "    foreach ($g in $o.Groups) { $otherOrgGroups += (\"{0}: {1}\" -f $o.Name, $g.Name) } " ^
    "} " ^
    "if ($otherOrgGroups) { $output.data.custom.alarmGroupsOther = ($otherOrgGroups -join \"`n\") } " ^
    "$jsonOut = $output | ConvertTo-Json -Depth 10 -Compress; " ^
    "Invoke-RestMethod -Uri 'http://127.0.0.1:83/rest/external/http/alarm/v2' -Method POST -Body $jsonOut -ContentType 'application/json'"

endlocal
