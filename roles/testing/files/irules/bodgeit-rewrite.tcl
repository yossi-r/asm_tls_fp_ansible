when HTTP_REQUEST {
	if { [HTTP::host] equals "jc-demof5-wp01-pip.westus2.cloudapp.azure.com" and [HTTP::uri] starts_with "/broken" } {
		HTTP::redirect "http://isitthef5.com"
	}
}
