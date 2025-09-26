from html.parser import HTMLParser;
import os;
import time;

# Formato de ejemplo:
# Fecha del Indicador, Banco,   Compra,  Venta # En th
# 30-04-2025,         Banesco, 87,2028, 86,89  # En td
METADATA_STR=["Fecha", "Banco", "Precio de Compra",
              "Precio de Venta"];
class dolar_data_to_json(HTMLParser):
    def __init__(self, older_date, recent_date):
        self.begin_row=False;
        self.data_id=0;
        self.older_date=time.strptime(
            older_date, "%d/%m/%Y"
        );
        self.recent_date=time.strptime(
            recent_date, "%d/%m/%Y"
        );
        self.data={};
        for id_data in METADATA_STR:
            self.data[id_data]=[];
        super(dolar_data_to_json, self).__init__();
    
    def handle_starttag(self, tag, attrs):
        if tag=="td":
            self.begin_row=True;
    
    def handle_data(self, data):
        # No ha comenzado la tabla.
        if not self.begin_row:
            return;
        # Verificamos date_to
        if self.data_id==0:
            date=time.strptime(
                data,
                "%d/%m/%Y" if '/' in data else "%d-%m-%Y"
            );
            # Verificamos si no estamos en el rango
            # de las fechas pasadas.
            if (
                date<self.older_date or  date>self.recent_date
            ):
                self.data_id+=1;
                return;
        self.data[
            METADATA_STR[self.data_id]
        ].append(data);
        self.data_id+=1;
        if len(METADATA_STR)==self.data_id:
            self.data_id=0;
    def handle_endtag(self,tag):
        # Nos aseguramos de no tomar las demas etiquetas.
        if tag=="td":
            self.begin_row=False;
    def get_csv(self):
        pass;
    def get_json(self):
        pass;

if __name__=="__main__":
    test_html="";
    dir_now=os.path.dirname(os.path.realpath(__file__));
    with open(dir_now+"/test/price_test.html",'r') as f_test:
        test_html=f_test.read();
    html_data=dolar_data_to_json(
        "24/9/2025", "26/9/2025"
    );
    html_data.feed(test_html);
    print(html_data.data);
