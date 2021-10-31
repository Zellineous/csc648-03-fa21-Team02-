// Time period (in milliseconds) the session timeout notification will be displayed for,
// before the session ends and the user is logged out
var _sessionNotificationTimeoutMs = 0;
// Interval at which session heartbeat Ajax calls will be performed
var _sessionTimeoutMs = 0;
// URL of the logout page user will be transferred to on session end
var _logoutPageUrl = '';
// URL of the session timeout notification page to be displayed as a popup
var _sessionTimeoutNotificationPageUrl = '';

var _sessionTimeoutNotificationWindowWidth = 300;
var _sessionTimeoutNotificationWindowHeight = 200;

// Timer ID's
var _sessionTimerID;
var _notificationTimerID;
// Reference to the timeout notification popup window
var _sessionTimeoutNotificationWindow;

// Performs the setup of session heartbeat functionality for the page.
function SetupSessionTimeoutNotification(SessionNotificationTimeout, SessionTimeout, LogoutUrl, SessionTimeoutNotificationUrl) {
	_sessionNotificationTimeoutMs = SessionNotificationTimeout;
	_sessionTimeoutMs = SessionTimeout;
	_logoutPageUrl = LogoutUrl;
	_sessionTimeoutNotificationPageUrl = SessionTimeoutNotificationUrl;
	ResetSessionTimers();
}

// Shows a popup with session timeout notification message
function ShowSessionTimeoutNotification() {
	var left = (screen.width / 2) - (_sessionTimeoutNotificationWindowWidth / 2);
	var top = (screen.height / 2) - (_sessionTimeoutNotificationWindowHeight / 2);

	_sessionTimeoutNotificationWindow = window.open(_sessionTimeoutNotificationPageUrl,
                'sessionTimeoutNotification',
                'height=' + _sessionTimeoutNotificationWindowHeight + ',width=' + _sessionTimeoutNotificationWindowWidth + ',status=0,toolbar=0,location=0,menubar=0,resizable=0,scrollbars=1,top=' + top + ',left=' + left,
                true);
}

// Resets all the session heartbeat related timers
function ResetSessionTimers() {
	window.clearTimeout(_sessionTimerID);
	_sessionTimerID = window.setTimeout('LogoutSession()', _sessionTimeoutMs);

	window.clearTimeout(_notificationTimerID);
	_notificationTimerID = window.setTimeout('ShowSessionTimeoutNotification()', _sessionNotificationTimeoutMs);
}

function LogoutSession() {
	if (_sessionTimeoutNotificationWindow != null && !_sessionTimeoutNotificationWindow.closed) {
		_sessionTimeoutNotificationWindow.close();
	}

	window.location = _logoutPageUrl;
}