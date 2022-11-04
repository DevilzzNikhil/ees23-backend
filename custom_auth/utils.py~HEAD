from datetime import datetime
from django.core.mail import EmailMessage

part1="""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verification</title>
    <style>
    div{
        border: 2px solid black;
        text-align: center;
    }
    h1{
        background-color: black;
        color:rgb(55, 199, 204);        
        font-size: 40px;
        margin-top: 0px;
    }
    h3{
        font-weight: 100;
    }
    a{
        background-color: blue;
        border-radius: 10px;
        font-size: 18px;
        color: rgb(248, 240, 240)!important;
        text-decoration: none;
        padding: 5px 10px;
        font-weight: 600;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    }
    </style>
</head>
<body>
    <div>
    <h1>UDYAM22</h1>
    <h3>Hi """

part2="""!</h3><h3>"""
part3="""</h3>
    <a href='"""
part4="""'>Verify Now</a>
    <h3>Please ignore if not filled by you.</h3>
    </div>
    <span style="color: #FFF; display: none; font-size: 8px;">""" +str(datetime.now())+"""</span>
</body>
</html>"""

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_mail']]
        )
        email.content_subtype='html'
        email.send()
