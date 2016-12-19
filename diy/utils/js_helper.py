# coding:utf-8


def js_alert(msg):
	return '<script>alert("%s")</script>'%msg

def js_alert_j_new(msg, jumpLocation="/wx_mgt"):
	# todo:need confim
	# return '<script>alert("%s");window.open("%s")</script>' % (msg,jumpLocation)
	return '<script>alert("%s");window.opener.location.href="%s"</script>' % (msg,jumpLocation)

def js_alert_refresh(msg, refresh="/wx_mgt"):
	return '<script>alert("%s");window.opener.location.href="%s"</script>' % (msg,refresh)