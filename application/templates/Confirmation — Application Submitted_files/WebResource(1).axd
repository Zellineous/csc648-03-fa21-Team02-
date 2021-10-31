var _clickCount = 0;

function DisableMulticlick()
{
	if (typeof (Page_ClientValidate) == 'function')
	{
		if (Page_ClientValidate() == true)
		{
			return CheckClick();
		}
		else
		{
			return true;
		}
	}
	else
	{
		return CheckClick();
	}
}

function CheckClick()
{
	if (_clickCount == 0)
	{
		_clickCount++; return true;
	}
	else
	{
		return false;
	}
}