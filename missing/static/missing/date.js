// Based on http://djangosnippets.org/snippets/84/

String.prototype.zfill = function (width) {
    var str = '' + this;
    while (str.length < width) str = '0' + str;
    return str;
};

String.prototype.toTitleCase = function () {
    return this.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
};

Date.prototype.strfdate = function (format) {
    // TODO: It returns based on current locale of the browser, not on possible different current locale user has configured for herself on the website/server/profile

    var dt = this;

    var year = dt.getFullYear();
    var month = dt.getMonth();
    var date = dt.getDate();
    var hours = dt.getHours();
    var minutes = dt.getMinutes();
    var seconds = dt.getSeconds();
    var milliseconds = dt.getMilliseconds();
    var day = dt.getDay();
    var offset = dt.getTimezoneOffset();

    var pieces = [];
    var piece;
    for (var c = 0; c < format.length; c++) {
        if (format[c] == '\\') {
            c += 1;
            piece = format[c];
        }
        else {
            try {
                var formatter = 'format_' + format[c] + '()';
                piece = eval(formatter);
            }
            catch (e) {
                piece = format[c];
            }
        }
        pieces.push(piece);
    }
    return pieces.join('');

    function format_a() {
        if (hours > 11) return gettext('p.m.');
        return gettext('a.m.');
    }

    function format_A() {
        if (hours > 11) return gettext('PM');
        return gettext('AM');
    }

    function format_b() {
        var MONTHS_3 = [
            gettext('jan'), gettext('feb'), gettext('mar'), gettext('apr'), gettext('may'), gettext('jun'),
            gettext('jul'), gettext('aug'), gettext('sep'), gettext('oct'), gettext('nov'), gettext('dec')
        ];
        return MONTHS_3[month];
    }

    /* function format_B() { Not implemented } */

    function format_c() {
        var offset_hours = ('' +  Math.floor(offset / 60)).zfill(2);
        var offset_minutes = ('' + (offset % 60)).zfill(2);
        var sign = (offset >= 0) ? '+' : '-';
        return dt.strfdate('Y-m-d\\TH:i:s.') + format_u().zfill(6) + (sign + offset_hours + ':' + offset_minutes);
    }

    function format_d() {
        return ('' + date).zfill(2);
    }

    function format_D() {
        var WEEKDAYS_ABBR = [
            gettext('Sun'), gettext('Mon'), gettext('Tue'), gettext('Wed'),
            gettext('Thu'), gettext('Fri'), gettext('Sat')
        ];
        return WEEKDAYS_ABBR[day];
    }

    /* function format_e() { TODO: To be implemented } */

    function format_E() {
        var MONTHS_ALT = [
            pgettext('alt. month', 'January'),
            pgettext('alt. month', 'February'),
            pgettext('alt. month', 'March'),
            pgettext('alt. month', 'April'),
            pgettext('alt. month', 'May'),
            pgettext('alt. month', 'June'),
            pgettext('alt. month', 'July'),
            pgettext('alt. month', 'August'),
            pgettext('alt. month', 'September'),
            pgettext('alt. month', 'October'),
            pgettext('alt. month', 'November'),
            pgettext('alt. month', 'December')
        ];
        return MONTHS_ALT[month];
    }

    function format_f() {
        if (minutes == 0) return format_g();
        return format_g() + ':' + format_i();
    }

    function format_F() {
        var MONTHS = [
            gettext('January'), gettext('February'), gettext('March'), gettext('April'), gettext('May'), gettext('June'),
            gettext('July'), gettext('August'), gettext('September'), gettext('October'), gettext('November'), gettext('December')
        ];
        return MONTHS[month];
    }

    function format_g() {
        if (hours == 0) return '12';
        if (hours > 12) return ('' + (hours - 12));
        return ('' + hours);
    }

    function format_G() {
        return ('' + hours);
    }

    function format_h() {
        return format_g().zfill(2);
    }

    function format_H() {
        return format_G().zfill(2);
    }

    function format_i() {
        return ('' + minutes).zfill(2);
    }

    /* function format_I() { TODO: To be implemented } */

    function format_j() {
        return ('' + date);
    }

    function format_l() {
        var WEEKDAYS = [
            gettext('Sunday'), gettext('Monday'), gettext('Tuesday'), gettext('Wednesday'),
            gettext('Thursday'), gettext('Friday'), gettext('Saturday')
        ];
        return WEEKDAYS[day];
    }

    function format_L(mod) {
        var y = typeof mod === 'undefined' ? year : year + mod;
        return y % 4 == 0 && (y % 100 != 0 || y % 400 == 0);
    }

    function format_m() {
        return format_n().zfill(2);
    }

    function format_M() {
        return format_b().toTitleCase();
    }

    function format_n() {
        return ('' + (month + 1));
    }

    function format_N() {
        var MONTHS_AP = [
            pgettext('abbrev. month', 'Jan.'),
            pgettext('abbrev. month', 'Feb.'),
            pgettext('abbrev. month', 'March'),
            pgettext('abbrev. month', 'April'),
            pgettext('abbrev. month', 'May'),
            pgettext('abbrev. month', 'June'),
            pgettext('abbrev. month', 'July'),
            pgettext('abbrev. month', 'Aug.'),
            pgettext('abbrev. month', 'Sept.'),
            pgettext('abbrev. month', 'Oct.'),
            pgettext('abbrev. month', 'Nov.'),
            pgettext('abbrev. month', 'Dec.')
        ];
        return MONTHS_AP[month];
    }

    /* function format_o() { TODO: To be implemented } */

    function format_O() {
        var offset_hours = ('' +  Math.floor(offset / 60)).zfill(2);
        var offset_minutes = ('' + (offset % 60)).zfill(2);
        var sign = (offset >= 0) ? '+' : '-';
        return (sign + offset_hours + offset_minutes);
    }

    function format_P() {
        if (minutes == 0 && hours == 0) return gettext('midnight');
        if (minutes == 0 && hours == 12) return gettext('noon');
        return format_f() + ' ' + format_a();
    }

    function format_r() {
        return dt.strfdate('D, j M Y H:i:s O');
    }

    function format_s() {
        return ('' + seconds).zfill(2);
    }

    function format_S() {
        if (date == 11 || date == 12 || date == 13) return 'th';
        var digit = date % 10;
        if (digit == 1) return 'st';
        if (digit == 2) return 'nd';
        if (digit == 3) return 'rd';
        return 'th';
    }

    function format_t() {
        var DAYS = [31, 28 + format_L(), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        return ('' + DAYS[month]);
    }

    /* function format_T() { TODO: To be implemented } */

    function format_u() {
        return ('' + (milliseconds * 1000));
    }

    function format_U() {
        return '' + Math.round(dt.getTime() / 1000);
    }

    function format_w() {
        return ('' + day);
    }

    function format_W() {
        var week_number;
        var jan1 = new Date();
        jan1.setDate(1);
        jan1.setMonth(0);
        jan1.setFullYear(year);
        var jan1_weekday = convertday(jan1.getDay()) + 1;
        var weekday = convertday(day) + 1;
        var day_of_year = parseInt(format_z());
        if (day_of_year <= (8 - jan1_weekday) && jan1_weekday > 4) {
            if (jan1_weekday == 5 || (jan1_weekday == 6 && format_L(-1))) {
                week_number = 53;
            }
            else {
                week_number = 52;
            }
        }
        else {
            if (format_L()) {
                var i = 366;
            }
            else {
                var i = 365;
            }
            if ((i - day_of_year) < (4 - weekday)) {
                week_number = 1;
            }
            else {
                var j = day_of_year + (7 - weekday) + (jan1_weekday - 1);
                week_number = Math.floor(j / 7);
                if (jan1_weekday > 4) {
                    week_number -= 1;
                }
            }
        }
        return ('' + week_number);

        function convertday(d) {
            return (7 + d - 1) % 7;
        }
    }

    function format_y() {
        return format_Y().slice(-2);
    }

    function format_Y() {
        return ('' + year);
    }

    function format_z() {
        var DAYS = [0, 31, 59 + format_L(), 90, 120, 151, 181, 212, 243, 273, 304, 334];
        var result = DAYS[month] + date;
        return ('' + result);
    }

    function format_Z() {
        return '' + (offset * 60);
    }
};
