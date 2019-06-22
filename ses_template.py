""" Dev: f97gp1@gmail.com (14/04/2019)

Class to create templates.

Using the boto API client for the Amazon SES.
"""
from time import gmtime, strftime
from sqlclient import dbMaker
import boto3
import json
import os
import re

class TemplateSender():

    def __init__(self, templateData=""):
        """
        Constructor of the class:

        @tempplateData dictionary: The structure need to follow this
        syntax:
            {
                "item":[
                    {"Url" : "url", "Image" : "img"},   
                    {"Url" : "url", "Image" : "img"},
                ]
            }
        that parameter will be contain data for the notifications
        """
        try:
            self.key_id = os.environ['aws_access_key_id']
            self.secret_id = os.environ['aws_secret_access_key']
            self.aws_id = os.environ['aws_account_id']
            self.TemplateData = templateData
            self.text_content = ""
        except KeyError:
            print("No variables at the environment")
        
    def fill_atrs(self, fileroute):
        """Using a .json file it well be possible to
        complete the attributes need on the constructor.

        If the the constructor have a route for a file,
        then the attributes will be stored into the file.

        @param: fileroute, string.
        """
        try:
            with open(fileroute, "r") as f:
                attrs = json.loads(f.read())
                f.close()
            attrs_keys = list(attrs.keys())
            if "Source" in attrs_keys:
                self.source = attrs["Source"]
                self.raw_source = self.source.split(" ")[-1].replace("<", "").replace(">", "")
                self.reply_to = self.raw_source
            if "TemplateName" in attrs_keys:
                self.template_name = attrs["TemplateName"]
            if "Subject" in attrs_keys:
                self.subject_line = attrs["Subject"]
            if "HtmlSource" in attrs_keys:
                try:
                    html_route = os.getcwd() + attrs["HtmlSource"]
                    self.html_content = open(html_route).read()
                except FileNotFoundError:
                    print("File not found {}\n".format(html_route))
            if "TextContent" in attrs_keys:
                self.text_content = attrs["TextContent"]
            if "Recipents" in attrs_keys:
                self.Recipents = attrs["Recipents"]
            if "ReplyTo" in attrs_keys and self.reply_to != "":
                self.reply_to = attrs["ReplyTo"]
            if "AWSReg" in attrs_keys:
                self.aws_Reg = attrs["AWSReg"]
        except FileNotFoundError:
            print("File {} not found".format(fileroute))
            

    def start_client(self, awsreg=""):
        if awsreg != "":
            self.aws_Reg = awsreg
        self.ses = boto3.client(
            'ses', 
            region_name=self.aws_Reg,
            aws_access_key_id=self.key_id,
            aws_secret_access_key=self.secret_id
        )


    def create_template(self, templateName, subject, text, html):
        response = self.ses.create_template(
                        Template={
                            'TemplateName'  : templateName,
                            'SubjectPart'   : subject,
                            'TextPart'      : text,
                            'HtmlPart'      : html
                        }
        )
        print(response)


    def get_template(self):
        """
        To view the content for an existing template
        including the subject line, HTML body and plain text.
        
        Only the template name is required
        """
        response = self.ses.get_template(
            TemplateName = self.template_name
        )
        print(response)


    def list_templates(self):
        response = self.ses.list_templates(
            MaxItems=10
        )
        print(response)


    def update_template(self):
        response = self.ses.update_template(
            Template = {
                'TemplateName'  : self.template_name,
                'SubjectPart'   : self.subject_line,
                'TextPart'      : self.text_content,
                'HtmlPart'      : self.html_content
            }
        )
        print(response)


    def send_template(self, action=""):
        """Use a template to send email to
        recipients.

        If the html code have no variables inside it.
        can not be usefull use templates.

        @param action [OPTIONAL]: If this argument is:

            "update"

            first update the template instanced in the class
            and later the templates will be send.
        """
        if len(self.TemplateData["item"]) > 0:
            if action == "update":
                self.update_template()
            
            for recipent in self.Recipents:
                response = self.ses.send_templated_email(
                    Source=self.source,
                    Destination={
                        'ToAddresses': [
                            recipent
                        ],
                    },
                    SourceArn="arn:aws:ses:{}:{}:identity/{}".format(self.aws_Reg, self.aws_id, self.raw_source),
                    ReplyToAddresses=[
                        self.reply_to,
                    ],
                    Template=self.template_name,
                    TemplateData="{}".format(str(self.TemplateData).replace("\'", "\"") )
                )
                print(response)


    def get_template_variables(self):
        """Usefull for debugs. 

        Print the entire template used in the current
        instance of the class.
        """
        print(self.TemplateData)

if __name__ == '__main__':
    # Example of use -> python utils/ses_template.py < 'file.json'
    attr_route = os.getcwd() + "/utils/ses_atributes.json"
    notify = "new_notify.json"    
    data = []

    with open(notify, "r") as f:
        data = [json.loads(k) for k in f]
    if len(data) > 0:
        ses = TemplateSender(
            templateData={"model":data}
        )

    ses.fill_atrs(fileroute=attr_route)
    ses.send_template(action="update")
    # os.remove("new_notify.json")
