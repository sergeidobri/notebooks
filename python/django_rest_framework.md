# Django REST Framework (DRF) 

DRF обеспечивает программный протокол общения сервера и клиента. На стороне сервера создается программный интерфейс API.

DRF способен в ответ на GET-, POST-, DELETE-, PUT-... и так далее запросы от пользователя, отправлять ответ в виде JSON-файла.

Реальный API должен поддерживать:
- CRUD;
- Валидация и защита от атак;
- Авторизация и регистрация;
- Права доступа к данным через API.

Архитектура работы Django REST Framework:
1. Запрос от клиента обрабатывается маршрутизатором;
2. Маршрутизатор определяет вид запроса и представление, которое с ним связано;
3. Представления обрабатывают запросы и отправляют ответ пользователю;
4. Как правило, ответы нужно передавать в JSON, потому управление передается так называемым сериализаторам;
5. Сериализаторы формируют данные для ответа на API запрос, а также выполняют парсинг входной информации;

# Установка DRF

1. Ставим проект Django;
2. Выполняем миграции, создаем таблицы БД, подключив заранее Postgres. Напоминание:
- устанавливаем postgres на комп / сервер;
- создание для СУБД базы данных и суперпользователя;
- установить psycopg2, связывающий PostgreSQL и Django;
- подключить Postgres к проекту;
- выполнить миграции.
3. Создаем приложение в этом проекте, добавляя в список INSTALLED_APPS;
4. pip install djangorestframework;
5. Регистрируем приложение djangorestframework в проекте в INSTALLED_APPS (дописываем 'rest_framework');

# Создание представлений

в views.py создадим представление для обработки запросов к API. В ветке rest_framework.genericcs находится много базовых классов представления, используем ListAPIView.

Создадим serializer.py, где будем хранить сериализаторы. Они наследуются от базового класса serializers.ModelSerializer (from rest_framework import serializers).

Связываем класс представления с маршрутом

`serializer.py`:

```python
from rest_framework import serializers 
from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
```

`views.py`:

```python
from rest_framework import generics
from .models import Candidate
from .serializers import CandidateSerializer

class CandidateAPIView(generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
```

`urls.py`:

```python
from django.urls import path
from .views import CandidateAPIView

urlpatterns = [
    path('candidatelist/', CandidateAPIView.as_view()),
]

```

В простейшем плане: класс представления использует сериализатор, задача которого дать ответ в виде json-строки

# Базовый класс APIView для представлений

Обработчики разных методов можно прописывать вручную, если класс представления будет наследоваться от базового класса APIView. Вообще все классы представлений в DRF наследуются от него, и в зависимости от своего функционала, по-разному перегружают обработчки методов. 

Функция model_to_dict() - преобразует модель в словарь, без байтовой сериализации

# Сериализатор. Класс Serializer

Роль сериализатора в DRF заключается в том, чтобы переводить данные, отправленные клиентом из формата json в модели и кверисеты и, наоборот, формировать из данных, полученных из базы (соответственно из объектов моделей и кверисетов), ответ в виде json файла.

Работа с сериализаторами DRF очень похожа на работу Django форм.

Принцип работы сериализатора в следующем: Пусть у нас есть модель с полями title и content. Тогда класс сериализатора будет наследоваться от serializers.Serializer и будет иметь те же самые поля, что и модель. Причем, у такого класса нужно подобрать правильные типы данных (ForeignKey - это IntegerField!!!!!), вот пример:

`serializers.py`:

```python
# модель
from rest_framework import serializers 
from rest_framework.renderers import JSONRenderer

class CandidateModel:
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
class CandidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()

def encode():
    candidate = CandidateModel('кандидат', 'номер 1')
    candidate_sr = CandidateSerializer(candidate)  # на этом этапе поля обрабатываются и создается словарик candidate_sr.data
    json = JSONRenderer().render(candidate_sr.data)
    return json
```

В сериализаторах можно удобно указывать стили, с которыми в будущем, полученные данные будут отображаться на странице браузера. Это делается аргументом style={'...':'...', ...}. Это очень похоже на widget=widgets.Textarea(attrs={...}) у форм в Django.
Декодирование:

```python 
def decode():
    stream = io.BytesIO(b'{"title":"Candidate","content":"number 1"}')
    data = JSONParser().parse(stream)
    serializer = WomenSerializer(data=data)
    serializer.is_valid()  # валидация данных
    print(serializer.validated_data)
```

Обработчик метода post:

```python
class CandidateAPIView(APIView):
    def post(self, request):
        serializer = CandidateSerializer()
```

![](images/image.png)

# Методы save(), create() и update() класса Serializer

Сериализаторы должны работать с базой данных. Не только получать все записи, но еще и добавлять их, изменять и удалять.

```markdown
* create(self, validated_data) - для добавления (создани) записи (данных);
* update(self, instance, validated_data) - для изменения данных (записи)
```

В момент вызова метода serializer.is_valid(raise_exception=True) формируется словарь validated_data, который и участвует в создании новой записи. Соответственно, измениния в бд мы сохраняем методом serializer.save()

```python
...
def post(self, request):
    serializer = CandidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)  # тут создается validated_data
    serializer.save()  # тут автоматически вызывается create() с параметром validated_data

    return Response({'post': serializer.data})  # теперь serializer будет ссылаться на только что созданный объект
```

В сериализаторе же:

```python
def create(self, validated_data):
    return Candidate.objects.create(**validated_data)
```

Для того, чтобы обновлять записи, перегрузим метод update. Делается это уже не так просто:

```python
def update(self, instance, validated_data):
    instance.title = validated_data.get("title", instance.title)
    ...  # для всех полей
    instance.save()
    return instance
```

```python
def put(self, request, *args, **kwargs):
```

# Класс ModelSerializer и представление ListCreateAPIView

Для работы с базой данных в Django Rest Framework существует сериализатор ModelSerializer, который существенно облегчает код.

`serializer.py`:

```python
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"
```

`views.py`:

```python
from rest_framework.views import APIView, Response
from .models import Candidate
from .serializers import CandidateSerializer


class CandidateAPIView(APIView):
    def get(self, request):
        candidates = Candidate.objects.all()
        return Response({'candidates': CandidateSerializer(candidates, many=True).data})
    
    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'candidate': serializer.data})
```

Для представлений также существуют заготовленные упрощения:
* CreateAPIView - создание данных по POST-запросу;
* ListAPIView - чтение списка данных по GET-запросу;
* RetrieveAPIView - чтение конкретных данных (записи) по GET-запросу;
* DestroyAPIView - удаление данных (*записи) по DELETE-запросу;
* UpdateAPIView - изменение записи по PUT или PATCH-запросам;
* ListCreateAPIView - для чтения (по GET-запросу) и создания списка данных по POST-запросу;
* RetrieveUpdateAPIView - чтение и изменение отдельной записи (GET- и POST-запросу);
* RetrieveDestroyAPIView - чтение (GET-запрос) и удаление (DELETE-запрос) отдельной записи;
* RetrieveUpdateDestroyAPIView - чтение, изменение и добавление отдельной записи (GET-, PUT-, PATCH-, DELETE-запросы).

# Представления UpdateAPIView и RetrieveUpdateDestroyAPIView

Чтобы предоставить функционал ранее реализованного PUT-запроса, воспользуемся классом UpdateAPIVIew

```python
class CandidateAPIUPdate(generics.UpdateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer()
```

На этом этапе стоит иметь в виду, что не все записи будут доставаться из модели Candidate. Запросы в Django - ленивые, и выполняются по мере действительной надобности. 

Чтобы получить / изменить / удалить какую-то одну конкретную запись, существует представление RetrieveUpdateDestroyAPIView:

```python
class CandidateDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
```

Остается только привязать адрес url. Теперь такой адрес будет поддерживать GET-, PUT-, PATCH-, DELETE- запросы

Django REST предоставляет удобный внутрибраузерный инструмент для тестирования разных запросов, но, очевидно, в продакшн такое выставлять нельзя. Потому в settings.py делаем следующее:

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # эта строчка позволяет работать в браузере. Убрав ее - будет нельзя.
    ]
}
```

# ViewSet

Сейчас в коде программы на лицо дублирование кода. Это можно поправить с помощью ViewSet-ов. Рассмотрим ModelViewSet.

```python
from rest_framework import viewsets

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Women.objects.all()
    serializer_class = CandidateSerializer
```

В таком случае для этого ViewSet-а , url-маршрут будет выглядеть следующим образом:

`urls.py`:
```python
    path('candidatelist/', CandidateViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path('candidatedetail/<int:pk>/', CandidateViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    })),
```

Сейчас URL-маршруты выполняют очень клишированное действие. Для этого в DRF существуют так называемые роутеры.

```python
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'candidate', CandidateViewSet)
router.register(....)  # сколько угодно вьюсетов 
...
    path("", include(router.urls)),
```

viewsets.ReadOnlyModelViewSet - то же самое, что и ModelViewSet, только с одним лишь GET методом

# Роутеры. SimpleRouter() и DefaultRouter()

Единственное и основное отличие этих роутеров в том, что DefaultRouter() генерирует путь .../api/v1 . Если выполнить на него GET запрос, то в ответ мы получим все зарегистрированные в этом роутере маршруты

Эти роутеры для каждого URL-маршрута генерируют собственные имена, которые бывают полезны в разработке (к примеру в методе reverse). Эти имена генерируются автоматически по шаблону

```markdown
<basename>-list
<basename>-detail
и так далее
```

По умолчанию basename= имя модели, привязанная к сериализатору. Изменить это можно именованным параметром при регистрации маршрутов:

```python
router.register(r"candidate", CandidateViewSet, basename="candidates")
```

Если нам не хватает предоставляемых маршрутов и их функционала, то с помощью декоратора @action можно это исправить:

```python 
@action(methods=["get"], detail=False)  # определяем во ViewSet-е. detail здесь True - показывает одну запись по pk, False - показывает много записей без pk
def category(self, request):  
    cats = Category.objects.all()
    return Response({"cats": [c.name for c in cats]})
```

Порой в проектах есть необходимость получать не все записи из таблицы, а всего-лишь по какому-то условию. Это можно переопределить в методе get_queryset():

```python
# ViewSet
def get_queryset(self):
    return Candidate.objects.filter(...)
```

Сейчас будут возвращаться записи по заданному условию. Если же мы попробуем получить одну запись - будет ошибка. Поправим:

```python
# ViewSet
def get_queryset(self):
    pk = self.kwargs.get("pk")
    if pk:
        return Candidate.objects.filter(pk=pk)  # очень важно использовать именно filter, не get
    else:
        return Candidate.objects.filter(...)  # условие
```