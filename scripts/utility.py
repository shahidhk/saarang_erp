# _____________--- DAJAX Alert Message ---______________#
def show_alert(dajax_, type_, msg_):
    """
        Give an alert in the bootstrap styled alert which is in base.html
    """
    #dajax_.remove_css_class("#id_alert", "alert-success")
    #dajax_.remove_css_class("#id_alert", "alert-warning")
    #dajax_.remove_css_class("#id_alert", "alert-error")
    #dajax_.remove_css_class("#id_alert", "alert-info")
    #dajax_.remove_css_class("#id_alert", "hide")
    
    #dajax_.add_css_class("#id_alert", "alert-" + type_.lower())
    #dajax_.assign("#id_alert", "innerHTML", "<button type='button' class='close' onclick='javascript:js_alert_hide();'>&times;</button><strong>" + type_.upper() + "!</strong> " + msg_);
    
    dajax_.script("$.bootstrapGrowl('" + str(msg_) +
        """', {
            ele: 'body', // which element to append to
            type: '""" + str(type_) + """', // (null, 'info', 'error', 'success')
            offset: {from: 'top', amount: 50}, // 'top', or 'bottom'
            align: 'right', // ('left', 'right', or 'center')
            width: '300', // (integer, or 'auto')
            delay: 10000,
            allow_dismiss: true,
            stackup_spacing: 10 // spacing between consecutively stacked growls.
        });""")