Date.prototype.timesince = function (now, reversed) {
    var dt = this;

    var chunks = [
        [60 * 60 * 24 * 365, function (n) {return ngettext('year', 'years', n);}],
        [60 * 60 * 24 * 30, function (n) {return ngettext('month', 'months', n);}],
        [60 * 60 * 24 * 7, function (n) {return ngettext('week', 'weeks', n);}],
        [60 * 60 * 24, function (n) {return ngettext('day', 'days', n);}],
        [60 * 60, function (n) {return ngettext('hour', 'hours', n);}],
        [60, function (n) {return ngettext('minute', 'minutes', n);}]
    ];

    now = typeof now === 'undefined' ? new Date() : now;
    reversed = typeof reversed === 'undefined' ? false : reversed;

    var delta = reversed ? dt - now : now - dt;
    var since = Math.floor(delta / 1000);

    if (since <= 0) {
        // dt is in the future compared to now, stop processing
        return '0 ' + gettext('minutes');
    }

    for (var i = 0; i < chunks.length; i++) {
        var seconds = chunks[i][0];
        var name = chunks[i][1];

        var count = Math.floor(since / seconds);
        if (count != 0) break;
    }

    var s = interpolate(gettext('%(number)s %(type)s'), {'number': count, 'type': name(count)}, true);
    s.next_update = seconds * 1000;

    if (i + 1 < chunks.length) {
        // Now get the second item
        var seconds2 = chunks[i + 1][0];
        var name2 = chunks[i + 1][1];
        var count2 = Math.floor((since - (seconds * count)) / seconds2);
        if (count2 != 0) {
            s += interpolate(gettext(', %(number)s %(type)s'), {'number': count2, 'type': name2(count2)}, true);
            s.next_update = seconds2 * 1000;
        }
    }

    return s;
};

Date.prototype.timeuntil = function (now) {
    return this.timesince(now, true);
};

Date.prototype.naturaltime = function () {
    var dt = this;

    var now = new Date();

    if (dt < now) {
        var delta = now - dt;
        var seconds = Math.floor(delta / 1000);
        var minutes = Math.floor(seconds / 60);
        var hours = Math.floor(minutes / 60);
        var days = Math.floor(hours / 24);

        if (days != 0) {
            return interpolate(pgettext('naturaltime', '%(delta)s ago'), {'delta': dt.timesince(now)}, true);
        }
        else if (seconds == 0) {
            return gettext('now');
        }
        else if (seconds < 60) {
            return interpolate(ngettext('a second ago', '%(count)s seconds ago', seconds), {'count': seconds}, true);
        }
        else if (minutes < 60) {
            return interpolate(ngettext('a minute ago', '%(count)s minutes ago', minutes), {'count': minutes}, true);
        }
        else {
            return interpolate(ngettext('an hour ago', '%(count)s hours ago', hours), {'count': hours}, true);
        }
    }
    else {
        var delta = now - dt;
        var seconds = Math.floor(delta / 1000);
        var minutes = Math.floor(seconds / 60);
        var hours = Math.floor(minutes / 60);
        var days = Math.floor(hours / 24);

        if (days != 0) {
            return interpolate(pgettext('naturaltime', '%(delta)s from now'), {'delta': dt.timeuntil(now)}, true);
        }
        else if (seconds == 0) {
            return gettext('now');
        }
        else if (seconds < 60) {
            return interpolate(ngettext('a second from now', '%(count)s seconds from now', seconds), {'count': seconds}, true);
        }
        else if (minutes < 60) {
            return interpolate(ngettext('a minute from now', '%(count)s minutes from now'), {'count': minutes}, true);
        }
        else {
            return interpolate(ngettext('an hour from now', '%(count)s hours from now', hours), {'count': hours}, true);
        }
    }
};

Date.prototype.updatingNaturaltime = function (dom_or_selector) {
    var dt = this;

    var now = new Date();
    var seconds = Math.floor((now - dt) / 1000);

    if (seconds > 0) {
        if (seconds <= 60) {
            var msg = gettext("just now");
            msg.next_update = (seconds + 1) * 1000;
        }
        else {
            var msg = interpolate(pgettext('naturaltime', '%(delta)s ago'), {'delta': dt.timesince(now)}, true);
        }
    }
    else {
        if (-seconds <= 60) {
            var msg = gettext("less than minute from now");
            msg.next_update = (-seconds + 1) * 1000;
        }
        else {
            var msg = interpolate(pgettext('naturaltime', '%(delta)s from now'), {'delta': dt.timeuntil(now)}, true);
        }
    }

    if (typeof dom_or_selector !== 'undefined') {
        $(dom_or_selector).text(msg);
        setTimeout(function () {
            dt.updatingNaturaltime(dom_or_selector);
        }, msg.next_update);
    }

    return msg;
};
