class Student:
    epsilon = 1e-6
    def __init__ (self, id, name, grades):
        self.id = id
        self.name = name
        self.grades = grades
        self.avg = self.average()
        self.classification = self.process()

    def average(self):
        return (sum(self.grades) / len(self.grades))
    
    def process(self):
        if self.avg - 5 < self.epsilon:
            return "YEU"
        elif self.avg - 5 > self.epsilon and self.avg - 6.9 <= self.epsilon:
            return "TB"
        elif self.avg - 7 > self.epsilon and self.avg - 7.9 <= self.epsilon:
            return "KHA"
        elif self.avg - 8 > self.epsilon and self.avg - 8.9 <= self.epsilon:
            return "GIOI"
        else:
            return "XUAT SAC"
        
def main():
    n = int(input())
    students_list = []

    for i in range(n):
        name = input()
        grades = list(map(float, input().split()))
        id = f"HS{(i + 1):02d}"
        students_list.append(Student(id, name, grades))

    students_list.sort(key=lambda student: (student.avg, student.id), reverse=True)
    for student in students_list:
        print(f"{student.id} {student.name} {student.avg:.1f} {student.classification}")

if __name__ == "__main__":
    main()