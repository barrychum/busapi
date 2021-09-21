# busapi
https://data.gov.tw/datasets/search?p=1&size=10&rft=%E5%88%B0%E7%AB%99
https://data.gov.tw/dataset/123112
https://data.gov.tw/dataset/122907

https://motc-ptx-api-documentation.gitbook.io/motc-ptx-api-documentation/api-shi-yong/hmac

https://ptx.transportdata.tw/MOTC
https://ptx.transportdata.tw/MOTC#!/Advanced/BusApi_Station_NearBy


curl -X GET --header 'Accept: application/json' 
--header 'Authorization: hmac username="FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF", 
algorithm="hmac-sha1", headers="x-date", signature="t72K6MtclzCh8nPldvG7BE24Qlo="' 
--header 'x-date: Fri, 17 Sep 2021 04:25:28 GMT' --header 'Accept-Encoding: gzip' 
--compressed  'https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/NearBy?$filter=StopID%20eq%20'173762'&$top=3000&$spatialFilter=nearby(25.080379452260896%2C%20121.56586593927369%2C%201000)&$format=JSON'
