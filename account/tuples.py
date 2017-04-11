#choice User_group

class CATEGORY:
	STUDENT = 1
	TEACHER = 2
	EMPLOYER = 3

	SELECT = (
		(STUDENT, 'Student'),
		(TEACHER, 'Teacher'),
		(EMPLOYER, 'Employer'),
	)

	def value(self, n):
		return self.SELECT[n - 1][1]



#choice User english language
class LANG:
	A1 = 1
	A2 = 2
	B1 = 3
	B2 = 4
	C1 = 5
	C2 = 6

	SELECT = (
		(A1, 'A1 - Elementary'), 
		(A2, 'A2 - Pre-Intermediate'), 
		(B1, 'B1 - Intermediate'), 
		(B2, 'B2 - Upper intermediate'),
		(C1, 'C1 - Advanced'), 
		(C2, 'C2 - Proficient'),
	)

	def value(self, n):
		return self.SELECT[n - 1][1]



class SKILL:
	CHOOSE = 0
	LANGUAGE = 1
	FRAMEWORK = 2
	OTHER = 3

	SELECT = (
		(CHOOSE, 'Choose category'),
		(LANGUAGE, 'Language'), 
		(FRAMEWORK, 'Framework'), 
		(OTHER, 'Other'), 
	)

	def value(self, n):
		return self.SELECT[n][1]