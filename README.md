# EmailSender
Simple python script to send IMF formatted emails.

# Prerequisite
> pip3 install -r requirements.txt

# How to use
Launch a server in one terminal (replace hostname and port):
> python -m smtpd -n -c DebuggingServer hostname:port

Launch a client in another:
> ./sender.py -d directory_path [-s servername] [-p port] [--ssl] [-a|--attachment]

If using the 'attachment' option, your folder needs to contain a "attachment" folder
containing all your attachment. Your mails also need to have a "Attachment" header
like in the example below:

> Attachment: picture.png

# Edit
You can edit the hostname and port for your smtp client in sender.py.

Additional information about SMTP port:
There is 4 commonly used ports.
 - 25: (oldest), it should be already be used so you don't want to use it.
   It's a relay port, another reason why you don't want to use it for smtp submissions.
 - 587: default port for smtp submission, support TLS.  
        Use this port if you want SMTP packet to be shown on your pcap.
 - 465: used for SMTPS (SMTP over SSL), depreciated.
 - 2525: unoffical, used when 587 is busy.

# Troubleshooting
This program might crash if fields From/Sender/To contained international
characters (see issue #3)
Fix them by hand for now.


# Under construction
Prerequisite
> mkcert localhost

Launch SSL SMTP Server
> ./server_smtp.py

# Authors
Amandine Nassiri <amandine.nassiri@epita.fr>
https://github.com/AnSpake/EmailSender
