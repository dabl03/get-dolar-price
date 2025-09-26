from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.begin_row=False;
        self.data=[];
    def handle_starttag(self, tag, attrs):
        if tag=="tr":
            self.data.append([None]);
            self.begin_row=True;
    def handle_data(self, data):
        
        print("Encountered some data  :", data)

parser = MyHTMLParser()
parser.feed('<html><head><title>Test</title></head>'
'<body><h1>Parse me!</h1></body></html>')