# <font size=8>SQL课堂练习</font>
![alt text](1711960505263.jpg)

### <font size=6>关系代数</font>
<font face='楷体' size=5>
(1) Π<sub>姓名</sub>((Π<sub>学号</sub>((Π<sub>课程号</sub>(σ<sub>课程名='物理'</sub>（课程）))∞选课))∞学生)<br>
(2) Π<sub>教师号</sub>(教师)-(Π<sub>教师号</sub>(σ<sub>成绩<60</sub>(选课)))<br>
(3) Π<sub>学号</sub>(学生)-(Π<sub>学号</sub>(σ<sub>((Π<sub>教师号</sub>(σ<sub>教师名称='张三'</sub>))=选课.教师号)(选课)</sub>))

### <font size=6>SQL</font>
(1) 
``` 
CREATE TABLE 学生信息(
    学号 CHAR(20) NOT NULL PRIMARY KEY,
    姓名 VARCHAR(20) NOT NULL,
    选课数量 INT
)

INSERT INTO 学生信息(学号,姓名,选课数量)
SELECT 学生.学号,姓名,COUNT(DISTINCT 课程号) AS 选课数量 FROM 学生, 选课
WHERE 学生.学号=选课.学号
GROUP BY 课程.学号,课程.课程号
```
(2)
```
SELECT 姓名 FROM 学生
WHERE 姓名 LIKE '诸%' AND 姓名 NOT LIKE '诸葛%'
```
(3)
```
SELECT 学生.学号,姓名 FROM 学生
WHERE 学号 IN (SELECT 学号 FROM 选课 AS A
WHERE A.学号=学生.学号 AND A.成绩 >= (SELECT MAX(成绩) FROM 选课 AS B
WHERE A.课程号=B.课程号
GROUP BY 课程号))
```
(4)
```
SELECT 学号,课程号,选课时间 FROM 选课 AS A
WHERE 选课时间 = (SELECT MIN(选课时间) FROM 选课 AS B
WHERE B.学号 = A.学号 AND B.课程号 = A.课程号
GROUP BY 学号,课程号)
```
(5)
```
UPDATE 选课
SET 成绩=60
WHERE 选课时间 ！= (SELECT MIN(选课时间) FROM 选课 AS B
WHERE B.学号 = A.学号 AND B.课程号 = A.课程号
GROUP BY 学号,课程号)
```
(6)
```
SELECT 课程号 FROM 选课 AS A
WHERE EXISTS (SELECT * FROM 课程，(SELECT 课程号 FROM 选课 AS C
WHERE A.学号 = C.学号) AS TMP
WHERE 课程.课程号 = A.课程号 AND 课程.先修课程号 IN TMP AND 课程.课程号 NOT IN TMP)
```