import email
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)


class Test(db.Model):
	id = db.Column(db.Integer, primary_key=True)


class Member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True)
	password = db.Column(db.String(30))
	email = db.Column(db.String(50))
	join_date = db.Column(db.DateTime)
	'''		ONE TO MANY RELATIONSHIPS	'''
	orders = db.relationship('Order', backref='member', lazy='dynamic')
	courses = db.relationship('Course', secondary='user_courses', backref='member', lazy='dynamic')


	def __repr__(self):
		return f'<Member {self.username}>'


'''		ONE TO MANY RELATIONSHIPS	'''
class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Integer)
	member_id = db.Column(db.Integer, db.ForeignKey('member.id'))


'''		MANY TO MANY RELATIONSHIPS		'''
class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))


db.Table('user_courses',
	db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
	db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
	)


if __name__ == '__main__':
	app.run()

"""
For create the tables in the database:
	from application import db
	db.create_all()
"""


'''INSERTING DATA'''
anthony = Member(username='Anthony', password='secret', email='anthony@prettyprinted.com',join_date=date.today())
db.session.add(anthony)
db.session.commit()

michelle = Member(username='MichelleForever', password='mypassword', email='mforever@gmail.com',join_date=date.today())


'''		UPDATING DATA		'''
anthony.password = 'mynewsecretpassword'
db.session.commit()


'''		DELETING DATA		'''
db.session.delete(anthony)
db.session.commit()


'''		INTRO TO QUERIES		'''
zach = Member(username='Zach1', password='zachisthebest', email='zach@gmail.com', join_date=date.today())
db.session.add(zach)
db.session.commit()

results = Member.query.all()

for r in results:
	print(r.username)
	'''
	>>> Anthony
	>>> MichelleForever
	>>> Zack1
	'''

ant = Member.query.filter_by(username='Anthony').first()
print(ant.username)
'''>>> Anthony'''
print(ant.email)
'''>>> anthony@prettyprinted.com'''


michelle = Member.query.filter(Member.username == 'MichelleForever').first()
print(michelle.username)
'''>>> MicheleForever'''
print(michelle.password)
'''>>> mypassword'''
print(michelle.email)
'''>>> mforever@gmail.com'''


'''		GENERATIVE QUERIES		'''

q = Member.query
'''>>> <flask_alchemy.BaseQuery object at 0x7f34a34s85>'''
q = q.filter(Member.username == 'Zach1')
'''>>> <flask_alchemy.BaseQuery object at 0x7f34a3578s>'''

q.first()
'''>>> <Member 'Zach1'>'''

q.all()
'''[<Member 'Zach1'>]'''

q1 = Member.query
q2 = q1.filter(Member.username == 'Anthony')
q1.all()
'''>>> [<Member 'Anthony'>, <Member 'MichelleForever'>, <Member 'Zach1'>]'''

q2.all()
'''>>> [<Member 'Anthony'>]'''

q3 = q2.filter(Member.email == 'anthony@prettyprinted.com')
q3.all()
'''>>> [<Member 'Anthony'>]'''

q4 = q3.filter(Member.password == 'thispassworddoesntexist')
q4.all()
'''>>> []'''


'''		NOT EQUALS AND LIKE		'''

q = Member.query.filter(Member.username != 'Anthony').all()
'''>>> [<Member 'MichelleForever'>, <Member 'Zach1'>]'''

q2 = Member.query.filter(Member.email != 'zach@gamil.com').first()
'''>>> [<Member 'Anthony'>]'''

q2 = Member.query.filter(Member.email != 'zach@gamil.com').all()
'''>>> [<Member 'Anthony'>, <Member 'MichelleForever'>'''


like_query = Member.query.filter(Member.username.like('%nth%')).all()
'''>>> [<Member 'Anthony'>]'''



'''		IN AND NOT IN		'''

q = Member.query.filter(Member.username.in_(['Anthony', 'Zach1']))
'''>>> [<Member 'Anthony'>, <Member 'Zach1'>'''

q = Member.query.filter(~Member.username.in_(['Anthony', 'Zach1']))
'''>>> [<Member 'MichelleForever'>]'''


'''		NULL AND NOT NULL		'''
## adding a data with null values
karen = Member(username='Kar', password='karenismyname')
db.session.add(karen)
db.session.commit()

q = Member.query.filter(Member.email == None).all()
'''>>> [<Member 'Kar'>]'''

q = Member.query.filter(Member.email != None).all()
'''>>> [<Member 'Anthony'>, <Member 'MichelleForever'>, <Member 'Zach1'>]'''


'''		AND		'''

q = Member.query.filter(Member.username == 'Anthony').filter(Member.email == 'anthony@prettyprinted.com').all()
'''>>> [<Member 'Anthony'>]'''

q = Member.query.filter(Member.username == 'Anthony', Member.email == 'anthony@prettyprinted.com').all()
'''>>> [<Member 'Anthony'>]'''

q = Member.query.filter(db.and_(Member.username == 'Anthony', Member.email == 'anthony@prettyprinted.com')).all()
'''>>> [<Member 'Anthony'>]'''


'''		OR		'''

q1 = Member.query.filter(db.or_(Member.username == 'Anthony', Member.username == 'Zach1')).all()
'''>>> [<Member 'Anthony'>, <Member 'Zach1'>]'''


'''		ORDER BY		'''

q = Member.query.order_by(Member.username).all()


'''		LIMIT		'''

q = Member.query.limit(2).all()


'''		OFFSET		'''
'''		devuelve todo despues de los elementos que se especifiquen		'''

q = Member.query.offset(3).all()

'''		COUNT		'''

q = Member.query.count()


'''		INEQUALITY	'''

q = Member.query.filter(Member.id > 4).all()


'''		ONE TO MANY RELATIONSHIPS	(ver el codigo)'''

'''		ONE TO MANY QUERIES		'''

anthony = Member.query.filter(Member.username == 'Anthony').first()

order1 = Order(price=50, member_id=anthony.id)
db.session.add(order1)
db.session.commit()

anthony.orders.all()
'''>>> all the orders that belong to anthony'''

order2 = Order(price=200, member=anthony) ### funciona igual de bien si paso el miembro completo en vez del id
db.session.add(order2)
db.session.commit()


'''		MANY TO MANY RELATIONSHIPS	(ver el codigo)'''

'''		MANY TO MANY QUERIES		'''

course1 = Course(name='Course One')
course2 = Course(name='Course Two')
course3 = Course(name='Course Three')

db.session.add(course1)
db.session.add(course2)
db.session.add(course3)

db.session.commit()

course1.member
'''>>> []'''

anthony = Member.query.filter(Member.usename == 'Anthony').first()
michelle = Member.query.filter(Member.usename == 'MichelleForever').first()

course1.member.append(anthony)
course1.member.append(michelle)

db.session.commit()