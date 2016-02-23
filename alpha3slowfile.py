
"""
Это третья альфа-версия проекта "Акинатор"
Здесь не учтена графика
Также несколько однообразны вопросы программы.
Пока что программа работает некорректно при неправильном вводе данных
(что-либо отличное от да/нет/не знаю в вопросах)
Пока что в программе не везде, где надо используется рандом(при выборе вопроса)
Версию стоит проверить на баги
Пока что программа работает очень медленно(некоторые действия выполняются за O(n*n) вместо O(1)
Скоро добавим индексы.
Над всеми этими моментами будем работать.
Заметка о багах номер один: не стоит называть столбец INDEX
Заметка 2:cu1 = conn1.execute("SELECT IDCRE,IDCHAR,IND FROM CORRELATIONS WHERE IDCRE = :j AND IDCHAR = :num", {"j": j, "num": num})
(это пример подстановки переменных в выражение)
"""
import random
import sqlite3
# создание таблиц
'''
нам нужны 3 таблицы:
1)ID и имя животного(animals)
2)ID и название признака
3)Таблица с 4 столбцами: ID, животное, признак, обладает или нет
База нам вообще нужна для: a, l1, l2
'''
conn1 = sqlite3.connect('creatures.db')
cursor = conn1.cursor()
random.seed(version = 2)
print("Добрый день!")
print("Предлагаю такую игру: Вы загадываете животное")
print("Я задаю вопросы про него, и Вы можете отвечать да/нет/не знаю")
print("Предупреждаю сразу: скорее всего, я угадаю!")
print("Ну как, сыграем?!")


#создание списка животных
#l1 = ['кот','собака','обезьяна','медведь','крокодил'] # список животных
l1 = ['0']*500;
animalname = conn1.execute("SELECT NAME from ANIMALS")
ruun = 0       # бегун по массиву названий животных/признаков в начале
for row in animalname:
    l1[ruun] = row[0]
    ruun = ruun + 1
cn = conn1.execute("SELECT count(*) from ANIMALS");     # количество животных
n = cn.fetchone()[0];
lim = 30                        # лимит вопросов
#l2 = ['зелёный цвет','шерсть']  # список признаков
l2 = ['0']*500;
ruun = 0
charname = conn1.execute("SELECT NAME from CHARACTERISTICS")
for row in charname:
    l2[ruun] = row[0]
    ruun = ruun + 1
cm = conn1.execute("SELECT count(*) from CHARACTERISTICS") # количество признаков
m = cm.fetchone()[0];
corr = conn1.execute("SELECT * from CORRELATIONS")
a = [[0] * 500 for i in range(501)]  # матрица признаков: 1 = да, 0 = не знаю, -1 = нет
inddd = [[0] * 500 for i in range(501)] # матрица id пар (животное, признак) в последней таблице(пока не используется)
vop = min(lim, m);                   # количество вопросов
used = [0] * 500                     # использован ли данный вопрос
good = [1] * 500                     # допустимо ли данное животное
answ = [[0] * 500 for i in range(501)]  # матрица ответов юзера: answ[0][i] - номера признаков, answ[1][i] - значения признаков
used2 = [0] * 500                       # использовано ли данное животное(в конце, при выяснении, обладает ли оно новым признаком

"""
Далее идёт алгоритм генерации вопроса и отсеивания ненужных вариантов
"""
num = 0
for i in range(1,vop + 1):
    num = 0                         # номер выбираемого нами вопроса(определяется позже)
    while (used[num] == 1):
        num = num + 1
    num2 = 0 # считаем количество животных, для которых признак 0
    for j in range(0,n):
        cu1 = conn1.execute("SELECT IDCRE,IDCHAR,IND FROM CORRELATIONS WHERE IDCRE = :j AND IDCHAR = :num", {"j": j, "num": num})
        #cu1 курсор для выборок из таблицы
        for row in cu1:
            if ((row[2] == 0) and (good[j] == 1)):
                num2 = num2 + 1
    num3 = 0
    z = num
    for j in range(z + 1, m):
        num3 = 0;
        if (used[j] == 0):
            for k in range(0,n):
                cu1 = conn1.execute("SELECT IDCRE,IDCHAR,IND FROM CORRELATIONS WHERE IDCRE = :k AND IDCHAR = :j", {"k": k, "j": j})
                for row in cu1:
                    if ((row[2] == 0) and (good[k] == 1)):
                        num3 = num3 + 1;
            if (num3 < num2):
                num = j
                num2 = num3
    print("Вопрос ",i,":","Данное животное имеет ",l2[num],"?")
    used[num] = 1
    s = input() #ответ пользователя
    answ[0][i - 1] = num
    """
    Заполняем ответы и исключаем варианты
    """
    if (len(s) == 2):
        answ[1][i - 1] = 1                         
        for j in range(0,n):
            cu1 = conn1.execute("SELECT IDCRE,IDCHAR,IND FROM CORRELATIONS WHERE IDCRE = :v AND IDCHAR= :w",{"v": j,"w": num})
            for row in cu1:
                if (row[2] == -1):
                    good[j] = 0
    elif (len(s) == 3):
        answ[1][i - 1] = -1
        for j in range(0,n):
            cu1 = conn1.execute("SELECT IDCRE,IDCHAR,IND FROM CORRELATIONS WHERE IDCRE = :v AND IDCHAR= :w",{"v": j,"w": num})
            for row in cu1:
                if (row[2] == 1):
                    good[j] = 0
    else:
        answ[1][i - 1] = 0
"""
Теперь мы выводим окончательный ответ
"""
coun = 0    # это будет количество оставшихся животных
chosen = 0  # это будет номер выбранного животного
for i in range(0,n):
    coun += good[i]
if (coun == 1):
    for i in range(0,n):
        if (good[i]):
            print("Это ",l1[i])
            chosen = i
elif (coun == 0):
    u = [0]*500 # это список количеств совпавших с ответами признаков
    w = [0]*500 # это список номеров кандидатов
    kol = 0     # это будет максимальное количество совпавших признаков
    kol2 = 0
    coun2 = 0   # это будет количество кандидатов
    for i in range(0,n):
        kol2 = 0
        for j in range(0,vop):
            cu1 = conn1.execute("SELECT IDCRE,IDCHAR,IND FROM CORRELATIONS WHERE IDCRE = :u AND IDCHAR = :v", {"u": i, "v": answ[0][j]})
            for row in cu1:
                if ((answ[1][j] == 0) or (answ[1][j] == row[2])):
                    kol2 = kol2 + 1
        if (kol2 > kol):
            kol = kol2
        u[i] = kol2
    for i in range(0,n):
      if (u[i] == kol):
          coun2 = coun2 + 1
          w[coun2 - 1] = i
    v = random.randint(0, coun2 - 1)
    chosen = w[v]
    print("Это ",l1[w[v]])
else:
    w1 = [0]*500     #список кандидатов
    co = 0           #количество кандидатов
    for i in range(0,n):
        if (good[i]):
            co = co + 1
            w1[co - 1] = i
    v1 = random.randint(0, co - 1)
    chosen = w1[v1]
    print("Это ",l1[w1[v1]])
print("Верно?")
s2 = input()
if (len(s2) == 2):
    for i in range(0,vop):
        cu1 = conn1.execute("SELECT IDCRE,IDCHAR,IND FROM CORRELATIONS WHERE IDCRE = :j AND IDCHAR = :num", {"j": chosen, "num": answ[0][i]})
        for row in cu1:
            if (row[2] == 0):
                conn1.execute("UPDATE CORRELATIONS SET IND = :w WHERE IDCRE = :u AND IDCHAR= :v",{"w": answ[1][i],"u": chosen,"v": answ[0][i]})
            else:
                if (answ[1][i] != 0):
                    conn1.execute("UPDATE CORRELATIONS SET IND = :w WHERE IDCRE = :u AND IDCHAR= :v",{"w": answ[1][i],"u": chosen,"v": answ[0][i]})    
else:
    chosen2 = -1 # это номер животного, совпавшего с загаданным пользователем(если такое есть)
    print("А какое животное Вы на самом деле загадали?")
    s3 = input() # название животного от пользователя
    for i in range(0,n):
        if (s3 == l1[i]):
            chosen2 = i
    #первый случай: если у нас есть такое животное
    if (chosen2 > - 1): 
        for i in range(0,vop):
            cu1 = conn1.execute("SELECT IDCRE,IDCHAR,IND FROM CORRELATIONS WHERE IDCRE = :j AND IDCHAR = :num", {"j": chosen2, "num": answ[0][i]})
            if (row[2] == 0):
                conn1.execute("UPDATE CORRELATIONS SET IND = :w WHERE IDCRE = :u AND IDCHAR= :v",{"w": answ[1][i],"u": chosen2,"v": answ[0][i]})
            else:
                if (answ[1][i] != 0):
                   conn1.execute("UPDATE CORRELATIONS SET IND = :w WHERE IDCRE = :u AND IDCHAR= :v",{"w": answ[1][i],"u": chosen2,"v": answ[0][i]})
    else:
        """
        Добавляем новое животное 
        """
        n = n + 1
        #l1.append(s3)
        conn1.execute("INSERT INTO ANIMALS VALUES (:s3)",{"s3": s3})
        for i in range(0,m):
            conn1.execute("INSERT INTO CORRELATIONS VALUES (:a,:b,:c)",{"a": n - 1, "b": i, "c": 0})
        for i in range(0,vop):
            conn1.execute("UPDATE CORRELATIONS SET IND = :c WHERE IDCRE = :a AND IDCHAR = :b",{"a": n - 1, "b": answ[0][i],"c": answ[1][i]})
        # Теперь признак добавить просим
        print("Введите признак, которым данное животное имеет или не имеет")
        print("Желательно,чтобы Вы знали, имеет ли животное этот признак")
        s4 = input()
        bo = 0    # есть ли признак в таблице 0 = нет, 1 = есть
        for i in range(0,m):
            if (s4 == l2[i]):
                bo = 1
        if (bo == 0):
            #l2.append(s4)
            conn1.execute("INSERT INTO CHARACTERISTICS VALUES (:s4)",{"s4": s4})
            for i in range(0,n):
                conn1.execute("INSERT INTO CORRELATIONS VALUES (:a,:b,:c)",{"a": i, "b": m - 1, "c": 0})
            print("Вы добавили новый признак!")
            print("Мне бы очень хотелось узнать, какие животные им обладают...")
            print("Поэтому я задам Вам несколько вопросов")
            print("Обладает ли ",l1[n - 1]," добавленным Вами признаком?")
            s6 = input()
            if (len(s6) == 2):
                #a[n - 1][m] = 1
                conn1.execute("UPDATE CORRELATIONS SET IND = :w WHERE IDCRE = :u AND IDCHAR= :v",{"w": 1,"u": n - 1,"v": m})
            elif (len(s6) == 3):
                #a[n - 1][m] = -1
                conn1.execute("UPDATE CORRELATIONS SET IND = :w WHERE IDCRE = :u AND IDCHAR= :v",{"w": -1,"u": n - 1,"v": m})
            else:
                #a[n - 1][m] = 0
                conn1.execute("UPDATE CORRELATIONS SET IND = :w WHERE IDCRE = :u AND IDCHAR= :v",{"w": 0,"u": n - 1,"v": m})
            que = 5        # число вопросов
            for y in range(0,que):
                ask = random.randint(1, n - y - 1)    # какое из оставшихся животных мы спросим
                nu = 0
                indd = 0
                while(nu < ask):
                    if (used2[indd] == 0):
                        nu = nu + 1
                    if (nu < ask):
                        indd = indd + 1
                used2[indd] = 1
                print("Обладает ли ",l1[indd]," добавленным Вами признаком?")
                s5 = input()
                if (len(s5) == 2):
                    #a[indd][m] = 1
                    conn1.execute("UPDATE CORRELATIONS SET IND = :w WHERE IDCRE = :u AND IDCHAR= :v",{"w": 1,"u": indd,"v": m})
                elif (len(s5) == 3):
                    #a[indd][m] = -1
                    conn1.execute("UPDATE CORRELATIONS SET IND = :w WHERE IDCRE = :u AND IDCHAR= :v",{"w": -1,"u": indd,"v": m})
                else:
                    #a[indd][m] = 0
                    conn1.execute("UPDATE CORRELATIONS SET IND = :w WHERE IDCRE = :u AND IDCHAR= :v",{"w": 0,"u": indd,"v": m})
            m = m + 1
