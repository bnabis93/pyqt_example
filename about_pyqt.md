### PyQt5 Study

-----

#### PyQt Install (+ qt creator)

pyuic5 -x hello.ui -o hello_ui.py (ui -> py)



#### 임덕규 님 발표 요약(Pycon2017)

QWidget, 가장 기본적인 widget
​	window의 frame, titlebar 제공.
​	기본적인 출력처리
​	입력의 이벤트 처
​	위치, 크기등의 속성값
​	=> widget을 구성하는데 가장 기본적인 속성을 가지고 있는 widget이다.

최종 완성되는 widget은 상속의 상속의 상속을 받아 완성이 된다.
​	즉, 여러 클래스의 상속으로 인하여 원하는 widget을 만들게 된다.

시그널과 슬롯
​	(ios / os 개발 시 나오는 그 시그널인가?)
​	음… 함수, 혹은 객체들간의 소통을 위한 기능
​	슬룻이란 것은 시그널을 받아 실행하는 기능을 말한다.
​	

####Qt Creator / PyQt5 하다가 알게 된 것들

PyQt 공식 reference를 참조함.

##### label (label widget)

QLabel Widget. text or image를 넣을 수 있다.
https://doc.qt.io/qt-5/qlabel.html#details, QLabel documentation. 참조 바람

##### python Lambda function

lambda 는 일회성 function이라 보면 된다. (익명 함수라고도 한다)
휘발성 함수?̊̈ 라 생각하면 될 듯.
좀 더 pythonic 한 coding을 할 수 있다.

##### Widget과 view의 차이

widget은 main, view는 sub라고 보면 될 것 같다.


##### List view 와 Tree view

#####![img](http://doc.qt.io/qt-5/images/treemodel-structure.png)
tree view를 이해하기 위한 img. 흔히 옆에 +가 있어 이를 누르면 그 안에 있는 애들이 주르륵 나오는 형태로
많이 사용한다. 즉, 무엇인가 상위 개념이 존재하고, 그에 따른 하위 개념이 존재 할 때, 사용
(지금 나의 경우 폴더를 하나 불러오고, 그에 따른 이미지를 불러오게 사용해도 된다.)
#####![img](http://doc.qt.io/qt-5/images/windows-treeview.png)
이런식으로 사용된다.

다음은 List view에 대한 설명이다. 먼저 사용 예를 보도록 하자.
#####![img](http://doc.qt.io/qt-5/images/windows-listview.png)
위와 같이 사용을 한다. tree view와 비슷하지만 쓰임이 조금 다르다는것을 알 수 있다.
위는 file이 나열이고, tree view는 좀 더 큰 집합의 나열이라 봐도 될 것 같다. (자료구조 이야기는 안해도 될 듯)
나의 경우, data를 추가하면 view에 띄우는 것을 만들고 싶었으니, tree view보다는 **list view**가 어울리는 것 같다.


##### Reference

* https://gist.github.com/sigmadream/45050b2efbbd64582487, qt creator 설치
* https://www.youtube.com/watch?v=YUdlGBAPNrU , 임덕규님 Pycon 2017 발표
* https://opentutorials.org/module/544 , OpenTutorials,  
* http://pyqt.sourceforge.net/Docs/PyQt5/, PyQt5 official documentation.
* https://build-system.fman.io/pyqt-exe-creation/ python exe file.
* https://www.pythoncentral.io/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel/ listview example

