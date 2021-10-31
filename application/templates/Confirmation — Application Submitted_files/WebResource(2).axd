function OpenUrlInNewWindow(url, windowName, params)
{
	newWindow = window.open(url, windowName, params);
	if (window.focus)
	{
		newWindow.focus();
	}
}

function DisplayHelpInNewWindow(url)
{
	// Open help in new window all the time.
	newWindow = window.open(url, "", "height=600,location=0,menubar=0,resizable=1,scrollbars=1");
	if (window.focus)
	{
		newWindow.focus();
    }
    window.gtag("event", "help-click", {
        event_category: "UIO",
        event_label: window.location.pathname + " " + url
    });
}