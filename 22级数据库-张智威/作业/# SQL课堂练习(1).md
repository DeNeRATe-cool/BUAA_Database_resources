# <font size=8>SQL������ϰ</font>
![alt text](1711960505263.jpg)

### <font size=6>��ϵ����</font>
<font face='����' size=5>
(1) ��<sub>����</sub>((��<sub>ѧ��</sub>((��<sub>�γ̺�</sub>(��<sub>�γ���='����'</sub>���γ̣�))��ѡ��))��ѧ��)<br>
(2) ��<sub>��ʦ��</sub>(��ʦ)-(��<sub>��ʦ��</sub>(��<sub>�ɼ�<60</sub>(ѡ��)))<br>
(3) ��<sub>ѧ��</sub>(ѧ��)-(��<sub>ѧ��</sub>(��<sub>((��<sub>��ʦ��</sub>(��<sub>��ʦ����='����'</sub>))=ѡ��.��ʦ��)(ѡ��)</sub>))

### <font size=6>SQL</font>
(1) 
``` 
CREATE TABLE ѧ����Ϣ(
    ѧ�� CHAR(20) NOT NULL PRIMARY KEY,
    ���� VARCHAR(20) NOT NULL,
    ѡ������ INT
)

INSERT INTO ѧ����Ϣ(ѧ��,����,ѡ������)
SELECT ѧ��.ѧ��,����,COUNT(DISTINCT �γ̺�) AS ѡ������ FROM ѧ��, ѡ��
WHERE ѧ��.ѧ��=ѡ��.ѧ��
GROUP BY �γ�.ѧ��,�γ�.�γ̺�
```
(2)
```
SELECT ���� FROM ѧ��
WHERE ���� LIKE '��%' AND ���� NOT LIKE '���%'
```
(3)
```
SELECT ѧ��.ѧ��,���� FROM ѧ��
WHERE ѧ�� IN (SELECT ѧ�� FROM ѡ�� AS A
WHERE A.ѧ��=ѧ��.ѧ�� AND A.�ɼ� >= (SELECT MAX(�ɼ�) FROM ѡ�� AS B
WHERE A.�γ̺�=B.�γ̺�
GROUP BY �γ̺�))
```
(4)
```
SELECT ѧ��,�γ̺�,ѡ��ʱ�� FROM ѡ�� AS A
WHERE ѡ��ʱ�� = (SELECT MIN(ѡ��ʱ��) FROM ѡ�� AS B
WHERE B.ѧ�� = A.ѧ�� AND B.�γ̺� = A.�γ̺�
GROUP BY ѧ��,�γ̺�)
```
(5)
```
UPDATE ѡ��
SET �ɼ�=60
WHERE ѡ��ʱ�� ��= (SELECT MIN(ѡ��ʱ��) FROM ѡ�� AS B
WHERE B.ѧ�� = A.ѧ�� AND B.�γ̺� = A.�γ̺�
GROUP BY ѧ��,�γ̺�)
```
(6)
```
SELECT �γ̺� FROM ѡ�� AS A
WHERE EXISTS (SELECT * FROM �γ̣�(SELECT �γ̺� FROM ѡ�� AS C
WHERE A.ѧ�� = C.ѧ��) AS TMP
WHERE �γ�.�γ̺� = A.�γ̺� AND �γ�.���޿γ̺� IN TMP AND �γ�.�γ̺� NOT IN TMP)
```