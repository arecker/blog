var DOM = {
    panelLinks: $('.panel p').find('a'),
    subscribeButton: $('#subscribeButton'),
    subscribeEmail: $('#subscribeEmail'),
    subscribeMessage: $('#subscribeMessage'),
    subscribeFullText: $('#subscribeFullText')
}

function Filter(element) {
    var value = $(element).val().toUpperCase();

    DOM.panelLinks.each(function() {
        if ($(this).text().toUpperCase().search(value) > -1) {
            $(this).show();
            $(this).next().show();
        } else {
            $(this).hide();
            $(this).next().hide();
        }
    });
}

function SubscribeApp(){
    /*
        This is the email subscription app.
        Contacts a rest API with a valid email
        and returns response.
     */
    var self = this;

    self.GetStuff = function(){
        self.email = DOM.subscribeEmail.val();
        self.fullText = DOM.subscribeFullText.attr("checked");
        self.emailBox = DOM.subscribeEmail;
        self.subscribeMessage = DOM.subscribeMessage;
    }

    self.BindListenders = function(){
        DOM.subscribeButton.click(TrySend);
    }

    function TrySend(){
        self.GetStuff();
        RestoreClasses();
        if ( IsNotBS() ){
            LetItRip();
        } else {
            WarnBadInput();
        }
    }

    function LetItRip(){
        
        var key = "";
        try {
            key = APP_KEY;
        } catch(err) {
            alert('You are missing the APPKEY file.  This isn\'t going to work.')
            return;
        }

        data = {
            "email": self.email,
            "full_text": self.fullText
        }

        $.ajax({
            url: 'http://api.alexrecker.com/email/subscriber/add/?app=' + key,
            type: "POST",
            dataType: "json",
            data: JSON.stringify(data),

            beforeSend: function(){
                // wait it out
            },

            complete: function (jqXHR, textStatus) {
                switch (jqXHR.status) {
                    case 201:
                        NotifyAllGood();
                        break;
                    case 400:
                        NotifyAlreadySubscribed();
                        break;
                    default:
                        NotifySomethingBroke();
                }
            }

        });

    }

    function RestoreClasses(){
        self.subscribeMessage
            .removeClass('alert-warning')
            .removeClass('alert-success')
            .removeClass('alert-info')
            .removeClass('alert-error');
        self.emailBox.parent().removeClass('has-warning');
    }

    function IsNotBS(){
        var regExp = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return regExp.test(self.email) && self.email != '';
    }

    function WarnBadInput(){
        self.subscribeMessage.addClass('alert-warning');
        self.emailBox.parent().addClass('has-warning');
        self.subscribeMessage.html('Are you sure that\'s right?');
        DOM.emailBox.val('');
    }

    function NotifyAllGood(){
        self.subscribeMessage.addClass('alert-success');
        self.subscribeMessage.html('Sweet!  Thanks for signing up');
        DOM.emailBox.val('');
    }

    function NotifySomethingBroke(){
        self.subscribeMessage.addClass('alert-error');
        self.subscribeMessage.html('Ah hell.  Something broke.  Try later...');
        DOM.emailBox.val('');
    }

    function NotifyAlreadySubscribed(){
        self.subscribeMessage.addClass('alert-info');
        self.subscribeMessage.html('Whaat?  You\'re already subscribed, you dungus.');
    }

    // On Init
    self.BindListenders();
}

$(document).ready(function(){
    var subscribeApp = new SubscribeApp();
});