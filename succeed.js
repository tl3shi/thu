var tm;

function format_time(sec) {
    var h = Math.floor(sec / 3600);
    var m = Math.floor((sec % 3600) / 60);
    var s = sec % 3600 % 60;
    return sprintf('%02d:%02d:%02d', h, m, s);
}

function format_byte(n) {
    var f = function(k, s) {
        return sprintf('%.2f', n / k) + s;
    }
    if (n > 1e9) {
        return f(1e9, 'G');
    } else if (n > 1e6) {
        return f(1e6, 'M');
    } else if (n > 1e3) {
        return f(1e3, 'K');
    } else {
        return n + 'B';
    }
}

function myclock() {
    $('#clock').text(format_time(++tm));
    setTimeout("myclock()", 1000);
}

function do_logout() {
    var res = post('/cgi-bin/do_logout');
    var code = {
        'logout_ok': '连接已断开',
        'not_online_error': '您不在线上'
    }[res];

    if (code) {
        alert(code);
        window.close();
    } else {
        alert('操作失败');
    }
}

$(document).ready(function() {
    var a = $.url().attr('query').split(',');
    $('#uname').text(a[1]);

    var f = a[2] / 1000000000;
    var len = f > 50 ? 280 : f * 264 / 50;
    tm = Number(a[4]);

    $('#usage_value').css('width', len + 'px');
    $('#usage_flux').text(format_byte(a[2]));
    myclock();
});

