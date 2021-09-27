function Get-HMACHash {
    [CmdletBinding()]
    param (
        # Message to geneate a HMAC hash for
        [Parameter(Mandatory = $true,
            Position = 0,
            ParameterSetName = "Default",
            ValueFromPipelineByPropertyName = $true)]
        [ValidateNotNullOrEmpty()]
        [String]
        $Message,
        # Secret Key
        [Parameter(Mandatory = $true,
            Position = 1,
            ParameterSetName = "Default",
            ValueFromPipelineByPropertyName = $true)]
        [ValidateNotNullOrEmpty()]
        [Alias("Key")]
        [String]
        $Secret,
        # Algorithm
        [Parameter(Mandatory = $false,
            Position = 2,
            ParameterSetName = "Default",
            ValueFromPipelineByPropertyName = $true)]
        [ValidateSet("MD5", "SHA1", "SHA256", "SHA384", "SHA512")]
        [Alias("alg")]
        [String]
        $Algorithm = "SHA256",
        # Output Format
        [Parameter(Mandatory = $false,
            Position = 2,
            ParameterSetName = "Default",
            ValueFromPipelineByPropertyName = $true)]
        [ValidateSet("Base64", "HEX", "hexlower")]
        [String]
        $Format = "Base64"
    )


    $hmac = switch ($Algorithm) {
        "MD5" { New-Object System.Security.Cryptography.HMACMD5; break }
        "SHA1" { New-Object System.Security.Cryptography.HMACSHA1; break }
        "SHA256" { New-Object System.Security.Cryptography.HMACSHA256; break }
        "SHA384" { New-Object System.Security.Cryptography.HMACSHA384; break }
        "SHA512" { New-Object System.Security.Cryptography.HMACSHA512; break }
    }

    $hmac.key = [Text.Encoding]::UTF8.GetBytes($secret)
    $signature = $hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($message))

    $signature = switch ($Format) {
        "HEX" { ($signature | ForEach-Object ToString X2 ) -join '' }
        "hexlower" { ($signature | ForEach-Object ToString x2 ) -join '' }
        Default { [Convert]::ToBase64String($signature) }
    }
   
    return ($signature)
}
