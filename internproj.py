import tornado.ioloop
import tornado.web
import MySQLdb
from math import sin, cos, sqrt, atan2, radians


class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/myform" method="POST">'
                    'Enter location/LatLong eg: Mumbai or 19.07283, 72.88261'
                   '<input type="text" name="lat">'
                   '<input type="text" name="long">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        db = MySQLdb.connect("localhost","root","root","interproj" )
        cursor = db.cursor()
        cursor.execute("SELECT * from place_temples")
        data = cursor.fetchall()
        self.write("You entered: " + self.get_body_argument("lat") + ", " + self.get_body_argument("long") + "\n")
        self.write("Temples within 20km vicinity are: " + "\n\n")
        for key in data:
            R = 6373.0
            lat1 = radians(key[1])
            lon1 = radians(key[2])
            lat2 = radians(float(self.get_body_argument("lat")))
            lon2 = radians(float(self.get_body_argument("long")))
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            if distance <= 20:
                self.write(key[3] + "\n")
        db.close()


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/myform", MyFormHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
