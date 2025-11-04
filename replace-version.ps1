Set-Location ./versioning
$ActualVersion = & { python -m setuptools_git_versioning }
Write-Output $ActualVersion
