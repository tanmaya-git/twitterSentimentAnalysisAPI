import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123456789",
  database="test"
)

mycursor = mydb.cursor()


sql = "INSERT INTO twitter (Tweets , Name , ScreenName ,Location , Place, len , ID , Date, Source , Likes,  RTs, SA ) VALUES ("Hello","Sarah", "Sarah", "Location", "Place", 0 , "123" ,"2018-11-14", "Mobile", 1 , 1 , 0 )"
mycursor.executemany(sql)
mydb.commit()

print(mycursor.rowcount, "record was inserted.")
