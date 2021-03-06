#choice User_group

class CATEGORY:
	STUDENT = 1
	TEACHER = 2
	EMPLOYER = 3

	SELECT = (
		('', '-----'),
		(STUDENT, 'Студент'),
		(TEACHER, 'Викладач'),
		(EMPLOYER, 'Роботодавець'),
	)

	def value(self, *args):
		return self.SELECT[args[0]][1]



#choice User english language
class ENGLISH:
	A1 = 1
	A2 = 2
	B1 = 3
	B2 = 4
	C1 = 5
	C2 = 6

	SELECT = (
		(A1, 'Низький: A1 - Elementary'), 
		(A2, 'Низький: A2 - Pre-Intermediate'), 
		(B1, 'Середній: B1 - Intermediate'), 
		(B2, 'Середній: B2 - Upper intermediate'),
		(C1, 'Високий: C1 - Advanced'), 
		(C2, 'Високий: C2 - Proficient'),
	)

	def value(self, *args):
		return self.SELECT[args[0] - 1][1]