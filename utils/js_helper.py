# coding:utf-8


def js_alert(msg):
	return '<script>alert("%s")</script>'%msg

def js_alert_refresh(msg, location="/wx_mgt"):
	script='<script>alert("%s");window.window.location.href="%s"</script>' % (msg,location)
	return script

