/**
 * Created by neoo on 2016/11/10.
 */
if (top != self) {
    top.location = self.location
}
function callBackBridge() {
    $("#altContent01_parent").hide();
    $("#altContent02_parent").children(0).attr("width", "1250px")
}
function clearbidcookies() {
    var usernumber = $.cookie('bidnumber');
    if (usernumber) {
        $.cookie('bidnumber', '', {expires: -1});
        $.cookie('bidcount', '', {expires: -1});
        $.cookie('vdate', '', {expires: -1});
        $.cookie('clientId' + usernumber, '', {expires: -1});
        $.cookie('tradeserver', '', {expires: -1});
        $.cookie('informationserver', '', {expires: -1});
        $.cookie('webserver', '', {expires: -1});
        $.cookie('lcserver', '', {expires: -1})
    }
}
function checkCookies() {
    var usernumber = $.cookie('bidnumber');
    if (!usernumber)location.href = 'login.htm'; else {
        var userName = $.cookie('username');
        $("#spClientName").html(userName).attr("title", userName);
        $("#getNumber").html(usernumber);
        $("#spBidCount").html($.cookie('bidcount') + '次');
        $("#spVDate").html($.cookie('vdate'));
        var clientId = $.cookie('clientId' + usernumber);
        var tradeserverstr = $.cookie('tradeserver');
        var informationserverstr = '';
        var webserver = $.cookie('webserver');
        var pwd = $.cookie('pwd');
        var lcserver = '';
        var auctype = $("#hidtype").val();
        var flashvars = {
            uid: usernumber,
            uname: userName,
            clientId: clientId,
            tradeserverstr: tradeserverstr,
            informationserverstr: informationserverstr,
            webserverstr: webserver,
            lcserverstr: lcserver,
            auctype: auctype,
            pwd: pwd
        };
        var params = {
            menu: "false",
            scale: "noScale",
            allowFullscreen: "true",
            allowScriptAccess: "always",
            bgcolor: "",
            wmode: "transparent"
        };
        var attributes = {id: "testsocket"};
        swfobject.embedSWF("ws-2015-client.swf?p=1.1", "altContent01", "900", "450", "11", "expressInstall.swf", flashvars, params, attributes)
    }
}
jQuery(function ($) {
    checkCookies()
});
function flashCallingCheck() {
    var Sys = {};
    var ua = navigator.userAgent.toLowerCase();
    var s;
    (s = ua.match(/msie ([\d.]+)/)) ? Sys.ie = s[1].split(".")[0] : (s = ua.match(/edge\/([\d.]+)/)) ? Sys.edge = s[1].split(".")[0] : (s = ua.match(/firefox\/([\d.]+)/)) ? Sys.firefox = s[1].split(".")[0] : (s = ua.match(/chrome\/([\d.]+)/)) ? Sys.chrome = s[1].split(".")[0] : (s = ua.match(/opera.([\d.]+)/)) ? Sys.opera = s[1].split(".")[0] : (s = ua.match(/version\/([\d.]+).*safari/)) ? Sys.safari = s[1].split(".")[0] : 0;
    if (Sys.ie) {
        if (Sys.ie < 6) {
            gotoLogin();
            return false
        } else {
            return true
        }
    } else if (Sys.edge) {
        return true
    } else if (!!window.ActiveXObject || "ActiveXObject" in window) {
        return true
    } else if (Sys.firefox) {
        gotoLogin();
        return false
    } else if (Sys.chrome) {
        gotoLogin();
        return false
    } else if (Sys.opera) {
        gotoLogin();
        return false
    } else if (Sys.safari) {
        return true
    }
}
function gotoLogin() {
    location.href = "login.htm"
}