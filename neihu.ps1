
$urlbase="https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/"
$urlparam = 'NearBy?$top=2000&$format=JSON&$spatialFilter=nearby(25.079478,121.568256,25)'
$url = $urlbase + $urlparam
# write-host $url
$poi = @("946","946sub")
$r = Invoke-RestMethod -Uri $url
foreach ($i in $r) {
    if ($i.RouteName.En -in $poi) {
        write-host $i.StopName.Zh_tw, $i.RouteName.En, ([math]::round(($i.EstimateTime / 60),1))
    }
}
# $j = ConvertTo-Json $r
# $j