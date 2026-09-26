class Student:
    def __init__(self,name,math,english,chinese):
        self.name=name
        self.math=math
        self.english=english
        self.chinese=chinese
    def __str__(self):
          return f'姓名: {self.name} |数学: {self.math} |英语: {self.english}|语文: {self.chinese}'
    def xg(self,chinese=None,english=None,math=None):
        if chinese is not None:
           self.chinese = chinese
        if math is not None:
            self.math = math
        if english is not None:
            self.english = english


class Education:
    student_list=[]
    def add(self):
        '''添加学生'''
        name=input('请输入学生姓名')
        for s in self.student_list:
            if s.name==name:
                print('已存在,添加失败')
                return
        chinese=int(input('请输入学生语文成绩'))
        math=int(input('请输入学生数学成绩'))
        english=int(input('请输入学生英语成绩'))
        if 0<=chinese<=100 and 0<=math<=100 and 0<=english<=100:
            s=Student(name,math,english,chinese)
            self.student_list.append(s)
            print('添加成功')
        else:
            print('数字需要在0~100之间')
            return
    def x_g(self):
        name=input('请输入修改学生的姓名')
        for s in self.student_list:
            if s.name==name:
                print(f'当前信息  {s}')
                chinese = int(input('请输入学生语文成绩'))
                math = int(input('请输入学生数学成绩'))
                english = int(input('请输入学生英语成绩'))
                if 0 <= chinese <= 100 and 0 <= math <= 100 and 0 <= english <= 100:
                    s.xg(math, english, chinese)
                    print('修改成功')
                    return
                else:
                    print('请输入0~100的数字')
                    return
        print('未找到该学生')
    def sc(self):
        name=input('请输入需要删除的学生姓名')
        for s in self.student_list:
            if s.name==name:
                self.student_list.remove(s)
                print('删除成功')
                return
        else:
            print('没有这个学生')
    def cx(self):
        name = input('请输入需要查询的学生姓名')
        for s in self.student_list:
            if s.name==name:
                print(f'学生信息{s}')
                return
        else:
            print('未找到该学生')
    def xs(self):
        for s in self.student_list:
            print(s)
    def xt(self):
        print('欢迎使用教育管理系统')
        while True:
            print('1.添加学生  2.修改学生  3.删除学生  4.查询指定学生  5.查询所有学生  6.退出系统')
            choice=int(input('请输入功能序号'))
            try:
                match choice:
                    case 1:
                        self.add()
                    case 2:
                        self.x_g()
                    case 3:
                        self.sc()
                    case 4:
                        self.cx()
                    case 5:
                        self.xs()
                    case 6:
                        print('Bye~')
                        break
                    case _:
                        print('请输入1~6的数字')
            except Exception as e:
                print('程序出错了,错误信息：',e)
a = Education()
a.xt()






