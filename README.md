# EmailSender
Simple python script to send IMF formatted emails.

# How to use
Launch a server in one terminal (replace hostname and port):
> python -m smtpd -n -c DebuggingServer hostname:port

Launch a client in another:
> ./sender.py -d directory_path [-s servername] [-p port]

# Edit
You can edit the hostname and port for your smtp client in sender.py.

Additional information about SMTP port:
There is 4 commonly used ports.
 - 25: (oldest), it should be already be used so you don't want to use it.
   It's a relay port, another reason why you don't want to use it for smtp submissions.
 - 587: default port for smtp submission, support TLS.
 - 465: used for SMTPS (SMTP over SSL), depreciated.
 - 2525: unoffical, used when 587 is busy.
