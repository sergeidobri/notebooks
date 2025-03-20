# Язык программирования C++

## Первая программа на С++

Комментарии в C++ можно ставить комментарий, как в C: //

Напишем первую программу:

```C++
#include <iostream>

int main()
{
    std::cout << "Hello, World!" << std::endl;

    return 0;
}
```

Здесь все понятно, кроме `std:: ...` . `std` здесь предопределяет пространство имен (namespace) стандартной библиотеки языка C++. Необходимо соблюдать такой синтаксис для обращения к объектам библиотек. В нашем случае `std::cout` - это объект класса `cout` стандартной библиотеки `std`

`std::endl` же - это функция, которая добавляет в текущий поток вывода символ переноса строки и очищает его [поток].


## Ввод-вывод с помощью объектов cin и cout

```markdown
cin - объект класса istream для работы с потоком stdin
cout - объект класса ostream для работы с потоком stdout
```

Чтобы пользоваться этими объектами, в программе должен быть подключен пакет `<iostream>`. Объекты `cin` и `cout` автоматически определяют формат читаемых данных по типу переменных, с которыми они записаны. 

Переопределенные операции:
- `<<`: __операция записи в выходной поток для объекта cout__.
- `>>`: __операция чтения из входного потока для объекта cin__.

```C++
#include <iostream>

int main()
{
    char str[100] = "Hi, Sergey!";
    short old = 99;
    double weight = 82.54;

    std::cout << str << "\n";
    std::cout << old << "\n";
    std::cout << weight << std::endl;

    return 0;
}
```

Под капотом это работает так: в C++ есть возможность переопределять операции для объектов классов. Для объекта `cout` эта операция перегружена для всех типов данных. Поэтому необязательно указывать тип при выводе данных в стандартный поток вывода.


```C++
#include <iostream>

int main()
{
    char str[100] = "Hi, Sergey!";
    short old = 99;
    double weight = 82.54;

    std::cin >> old;
    std::cin >> weight;

    return 0;
}
```

Обратите внимание, что мы опять не указывали типы данных. Дело в том, что для объекта `cin` в C++ переопределена операция `>>` для всех типов данных. Также эта операция использует __механизм ссылок__, потому взятие переменной по адресу, как это было в `scanf`, не требуется.

Если данные были введены некорректно, то в переменную запишется 0.

Помимо всего прочего, операция `>>` для объекта `cin` возвращает все тот же объект `cin`. Поэтому программу можно переписать так:

```C++
#include <iostream>

int main()
{
    char str[100] = "Hi, Sergey!";
    short old = 99;
    double weight = 82.54;

    std::cin >> old >> weight;

    return 0;
}
```

С вводом строк все сложнее: чтение идет до __пробельного символа__!

Для чтения целой строки из потока ввода, необходимо воспользоваться функцией `getline(cin, str)`, где `str` - соответственно объект класса `string`. Позже об этом поговорим

## Пространства имен (namespace)

Из языка C мы помним, что в глобальной области видимости можно создавать функции, переменные, структуры. В языке C++ все такие определения попадают в __глобальное пространство имён__, и в функции `main` мы можемм обращаться ко всем этим определениям из глобального пространства имён. Это можно сделать просто с помощью имени переменной, функции или структуры, определенной в глобальном пространстве, а можем через символ четырёхточия: `::`. Данный символ обращается к глобальному пространству (именно глобальному! Если локально была определена переменная с тем же именем, то символ четырехточия проигнорирует локальную переменную и будет обращаться к переменной в глобальном пространстве имён) имён в том случае, если перед ним нет никакого другого имени. В противном случае, переменная, функция, структура, объект и т.д. который используется в программе с оператором четырехточия будет искаться в заданном слева от него пространстве имён.

```C++
#include <iostream>

int foo(void) {
    return 1;
}

int main(void)
{
    ::foo();
    return 0;
}
```

При попытке создания функций с одинаковым именем и прототипами, мы столкнемся с ошибкой на этапе компиляции. Или, например, при подключении модулей, содержащих одинаковые прототипы функций с разными реализациями, мы увидем всё тот же конфлик имён. Именно по этой причине в С++ появилось понятие __пространства имён__. Это позволяет избавиться от таких конфликтов. Для такого функционала используется ключевое слово `namespace`:

```C++
#include <iostream>

namespace firstSpace {
void foo()
{
    std::cout << "function from firstSpace foo()" << std::endl;
}
}

namespace secondSpace {
void foo()
{
    std::cout << "function from secondSpace foo()" << std::endl;
}
}

int main()
{
    firstSpace::foo();
    secondSpace::foo();
    return 0;
}
```

При необходимости в пространство имён можно дописывать новые имена в любом месте программы, используя все тот же синтаксис.

В C++ можно определять вложенные пространства имён:

```C++
#include <iostream>

namespace firstSpace {
void foo()
{
    std::cout << "function from firstSpace foo()" << std::endl;
}

namespace nestedSpace {

int nested_a = 10;
}
}

int main()
{
    firstSpace::foo();
    std::cout << firstSpace::nestedSpace::nested_a << std::endl;
    return 0;
}
```

При использовании ключевого слово `inline` вместе с `namespace`, можно опускать вложенное пространство имён:

```C++
#include <iostream>

namespace firstSpace {
void foo()
{
    std::cout << "function from firstSpace foo()" << std::endl;
}

inline namespace nestedSpace {

int nested_a = 10;
}
}

int main()
{
    firstSpace::foo();
    std::cout << firstSpace::nestedSpace::nested_a << '\n';
    std::cout << firstSpace::nested_a << std::endl;
    return 0;
}
```

## Оператор using

Если некоторые имена из пространства имён нужны в тексте программы достаточно часто, то их можно импортировать в глобальное пространство при помощи оператора `using`. Использовать его можно в соответствии с вот таким синтаксисом:

```markdown
using <пространство имён>[::<элемент>];
```

Если прописать оператор `using` в локальной области видимости, например, в функции, то именно туда эти имена и будут импортированы.

Также у оператора `using` есть ещё одно применение:

```markdown
using <alias> = <тип данных>;
```

Например:

```C++
using byte_8 = unsigned char;
using DATA = test::VAR;
using PTR_STR = char*;
using AR_INT = int[10];
using UINT = unsigned int;
using VOLUME = struct {int width, height, depth;}; 
```

Чем же этот синтаксис отличается от `typedef`? Ничем. 😊 Есть одно незначительное синтаксическое отличие при определении указателя на функцию:

```C++
typedef float (*func)(int);
using func = float (*)(int);
```

## Новые типы данных. Приведение типов указателей

- __bool__ – булевый тип (1 байт), принимающий два состояния true/false  
- __wchar_t__ – расширенный символный тип (2 байта в ОС Windows; 4 байта в ОС Linux)  
- __char8_t__ – символный тип (1 байт) для символов кодировки Unicode (UTF-8) (добавлен в стандарте C++20)  
- __char16_t__ – символный тип (2 байта) для символов кодировки Unicode (UTF-16)  
- __char32_t__ – символный тип (4 байта) для символов кодировки Unicode (UTF-32)

```C++
#include <iostream>

using std::cout;
using std::cin;
using std::endl;

int main()
{
    bool fl_print = false;
    wchar_t wch;

    wch = L'Я';

    cout << wch << endl;
    cout << fl_print << endl;

    return 0;
} 
```

Отличие здесь языка C++ от C заключается в том, что символы представляются типом данных `char`, в отличии от `int` в C. Еще одно отличие заключается в приведении некоторых типов указателей:

```C++
int* ptr_i = 0L;
char* ptr_ch = 0L;
void* ptr = 0L;

ptr_i = ptr;  // ошибка на C++ , ничего не произошло бы в C
ptr_ch = ptr_i;  // ошибка на C++ , предупреждение в C
```

Соответственно, приводим типы в `malloc`. В отличии от C++ рекоммендуют использовать `0L` или `nullptr` (определен со стандарта C++11) вместо константы `NULL`, как это было в C

В языке C++ появилась новая форма цикла `for`:

```C++
#include <iostream>

using std::cout;

int main()
{
    char msg[] = "I like C++ language";

    for(char x : msg)
        cout << x << " ";
    return 0;
} 
```

На каждой итерации `x` копировал в себя элемент коллекции `msg`.

## Инициализация переменных. Ключевые слова auto и decltype

В языке C операция инициализации и операция присваивания происходят с помощью оператора `=`:

```C++
int main()
{
    int val = 0;  // инициализация
    int pow[] = {1, 2, 4, 8};

    double d;
    d = 5.78;  // присваивание

    return 0;
} 
```

Чтобы отделить __инициализацию__ и __присваивание__, в языке C++ ввели новые конструкции:

```C++
#include <iostream>

using std::cout;
using std::cin;
using std::endl;

int main()
{
    short sh(10);  // инициализация, функциональная нотация [functional notation]

    char ch{'b'};  // инициализация при помощи фиг. скобок [braced initialization]

    long lv{};  // инициализация нулем

    cout << sh << endl;
    cout << ch << endl;
    cout << lv << endl;

    return 0;
} 
```

В языке C++ инициализация начальных переменных - это __рекоммендуемая практика__, так как автоматические переменные задаются неопределенными значениями.

Чем же отличается _functional notation_ от _braced initialization_ ? Почти ничем, за исключением того, что _braced initialization_ дополнительно проводит сравнивание типов.

```C++
long lv(5.43);  // ошибки нет, 5.43 приводится к long и lv инициализируется пятеркой
long lv{5.43};  // ошибка компиляции, переменная типа lv инициализируется вещественным значением, что недопустимо
```

Ещё несколько примеров инициализации переменных:

```C++
int sum {2 + 3 + 4 + 5};
double p (1 * 2.3 * 4.5 - 1);
bool n_fl(false), t_fl(true);
```

Как мы знаем из курса языка C, с помощью ключевого слово (модификатора) `const`, мы можем объявлять переменные, значения которых не меняются. В С++ этот модификатор используется с теми же целями, но есть отличие: константная переменная должна быть сразу проинициализирована, в противном случае будет ошибка.

Начиная со стандарта C++11 ключевое слово `auto` радикально изменило своё значение. Раньше в языке C оно вводилось для явного обозначения автоматических переменных. Теперь же с его помощью можно определять переменные вычисляемого типа (такие переменные обязательно надо инициализировать):

```C++
int main()
{
    auto i = -100;      // тип unt
    auto d = 76.98;     // тип double
    auto g = 0.55f;     // тип float
    auto h = 'f';       // тип char

    return 0;
} 
```

Здесь есть ряд нюансов:

```C++
int main()
{
    int *ptr = nullptr;
    int k;
    int& lk = k;

    auto t1 = k;        // int
    auto t2 = *ptr;     // int
    auto t3 = ptr;      // int *
    auto t4 = &ptr;     // int **
    auto t5 = lk;       // int

    return 0;
} 
```

При добавлении модификатора `const`:

```C++
int main()
{
    const int *ptr = nullptr;
    const int k;
    const int& lk = k;

    auto t1 = k;        // int, предполагается, что мы с этой переменной будем работать как с обычным int, хоть k и const int
    auto t2 = *ptr;     // int
    auto t3 = ptr;      // const int *, константные указатели можно присваивать только константным указателям
    auto t4 = &ptr;     // const int **
    auto t5 = lk;       // int

    return 0;
} 
```

Чтобы оставить тип переменной полностью неизменным, можно воспользоваться `decltype`:

```C++
decltype(k) var1 = 1;
```

`decltype` возвращает полный тип без каких-либо изменений. 

У ключевого слова `auto` есть свои недостатки: 

- его нельзя использовать в ряде компиляторов при определении типов параметров функций.

## Ссылки. Константные ссылки

Мы можем инициализировать переменную и ссылку на эту переменную. Что значит ссылка? Где-то в области памяти размещается переменная `d`, и мы можем читать из этих ячеек памяти значение переменной `d` типа `int`, или записать в них что-то другое. Теперь с этими ячейками памяти связано еще имя помимо имени `d`: `lnk_d`. Связь ссылки с ячейками памяти происходит в момент ее инициализации, поэтому инициализация обязательна.

```C++
#include <iostream>

using std::cout;
using std::cin;
using std::endl;

int main()
{
    int d = 10;
    int& lnk_d = d;  // ссылка, которая ссылается на переменную d

    cout << lnk_d;

    lnk_d = -5;
    cout << d;

    return 0;
} 
```

В некотором смысле ссылку можно воспринимать как неявный указатель, который хранит адрес переменной, записанной при инициализации. Причем при инициализации можно прописывать любые `lvalue` выражения, т.е. выражения, связанные с любыми ячейками памяти, в которые можно что-то записывать и считывать из них информацию. Вот примеры правильных и неправильных ссылок:

```C++
int a = 1;
int *ptr = &a;
int ar[] = {1, 2, 3};

int& lnk_1 = a;       // ok
int& lnk_2 = *ptr;    // ok
int& lnk_3 = ar[1];   // ok
int& lnk_4 = 10;      // ошибка
int& lnk_5 = ptr;     // ошибка
```

В чем же преимущество использования ссылок? Польза проявляется там же, где и указатели: в функциях. Рассмотрим пример:

```C++
#include <iostream>

using std::cout;
using std::endl;

void swap_d(double& x, double& y)
{
    double t = x;
    x = y;
    y = t;
}

int main()
{
    double a{1.2}, b{-3.4};
    swap_d(a, b);

    cout << a << " " << b << endl;

    return 0;
}
```

При передачи переменных в функции при помощи ссылок, во-первых, увеличивается безопасность и читаемость программы в отличие от использования указателей, а также, как и в случае с указателями, копирования большого числа данных не происходит. Ссылка в функции ссылается на аргумент функции, без процесса копирования.

Также ссылкам можно найти, например, такое применение: 

```C++
#include <iostream>

using std::cout;
using std::endl;

int main()
{
    int p[] = {1, 2, 3, 4, 5};

    for(int& x : p)
        x *= 2;

    for(int x : p)
        cout << x << ' ';

    cout << endl;

    return 0;
}
```

В языке C++ можно объявлять константные ссылки. Ячейки памяти, на которые ссылаются такие ссылки можно читать, но нельзя изменять. Такие ссылки можно инициаилизировать обычными, а также константными переменными. Но обычные ссылки нельзя инициализировать константными данными.

```C++
#include <iostream>

using std::cout;
using std::endl;

int main()
{
    int s = 0;
    const int& ls = s;

    int x = ls;
    // ls = -2;  // нельзя изменить значение
    cout << x << endl;

    return 0;
}
```

## Объект-строка string. Операции с объектами класса string

В языке C со строками было работать очень неудобно. В C++ же появлиась возможность работать с объектами класса `string`. Для этого нужно подключить заголовок `<string>`

После этого в пространстве имён `std` будет доступен класс `string`. Он использует при своей работе динамический массив символов

```C++
#include <iostream>
#include <string>

int main()
{
    std::string msg;  // msg - объект класса std::string. Сейчас msg = "", т.е. маркер конца строки

    std::cout << msg << std::endl;
    
    const char* data = msg.data();

    std::string msg2 {"Hello, Sergey Balakirev!"};
    std::string fio {"Sergey Balakirev!"};
    std::string fio_new {fio};

    fio_new[5] = 'i';
    std::cout << fio_new << std::endl;

    for(const char& ch : fio)
        std::cout << ch << ' ';
    std::cout << std::endl;

    return 0;
}
```

У объектов класса `string` есть методы `.size()` - фактическое количество символов в строке, `.capacity()` - размер динамического массива, `.data()` - возвращает одномерный массив из символов.

Для доступа к отдельным элементам строки можно по-прежнему использовать оператор `[]`.

Добавлять строки в конец можно с помощью метода `.append()`, или оператором сложения:


```C++
#include <iostream>
#include <string>

int main()
{
    std::string msg {"Hello"};
    std::string name {"Nice to see you"};
    msg.append(", Sergey!");

    std::cout << msg << std::endl;

    msg.append(" ");
    msg = msg + name;

    std::cout << msg << std::endl;

    return 0;
}
```

Вводить с клавиатуры строки можно при помощи `std::cin`. Чтение происходит до первого пробельного символа. Для чтения всей строки удобно воспользоваться функцией `getline(std::cin, msg);` (третьим, необязательным аргументом можно указать разделитель до которого будет читаться строка):

```C++
#include <iostream>
#include <string>

int main()
{
    std::string msg;
    std::cin >> msg;
    std::cout << msg << std::endl;
    getline(std::cin, msg);
    std::cout << msg << std::endl;

    return 0;
}
```

Функция `to_string()` конвертирует числа в строки:

```C++
#include <iostream>
#include <string>

using std::string;
using std::to_string;   // для конвертации чисел в строки
using std::cin;
using std::cout;
using std::endl;

int main()
{
	int width, height;
    
    cin >> width >> height;
    
    string data_str {"Переменная width = "};
    data_str = data_str + to_string(width);
    data_str.append(", переменная height = ");
    data_str = data_str + to_string(height);
    
    cout << data_str << endl;
    return 0;
}
```

Также можно объявлять __неизменяемые__ объекты строк.

## Файловые потоки. Открытие и закрытие файлов. Режимы доступа

В C++ есть такие классы, которые упрощают работу с файловыми потоками:

* __ifstream__ - для чтения данных из файла;
* __ofstream__ - для записи данных в файл;
* __fstream__ - для записи и чтения данных из файла.

Классы, которые работают с типом `wchar_t`:

* __wifstream__ - для чтения данных из файла;
* __wofstream__ - для записи данных в файл;
* __wfstream__ - для записи и чтения данных из файла.

Для работы с файловыми потоками нам необходимы объекты данных классов. После создания объектов, их нужно связать с определенными файлами. Для этого используется метод `.open(<путь до файла>)`, не забываем закрывать эти потоки: `.close()`

```C++
#include <iostream>
#include <fstream>

int main(void)
{
    std::ofstream ofs;
    std::ifstream ifs;

    ofs.open("ofs.dat");
    ifs.open("ifs.dat");

    ofs.close();
    ifs.close();

    return 0;
}
```

Связывать объект класса чтения или записи с определенным файловым потоком можно и в момент создания объекта:

```C++
#include <iostream>
#include <fstream>

int main(void)
{
    std::ofstream ofs("ofs.dat");
    std::ifstream ifs("ifs.dat");

    ofs.close();
    ifs.close();

    return 0;
}
```

Для проверки успешного открытия файла предусмотрен специальный метод `.is_open()`. Он возвращает истину, когда файл был успешно открыт, и ложь в противном случае.

```C++
#include <iostream>
#include <fstream>

int main(void)
{
    std::ofstream ofs("ofs.dat");
    std::ifstream ifs("ifs.dat");

    std::cout << (ofs.is_open() ? "Файл открыт" : "Файл не открыт") << std::endl;
    std::cout << (ifs.is_open() ? "Файл открыт" : "Файл не открыт") << std::endl;

    ofs.close();
    ifs.close();

    return 0;
}
```

Основные режимы доступа при открытии файла:

- __ios::in__ – для чтения (только для объектов классов ifstream или fstream)  
- __ios::out__ – для записи; прежние данные удаляются (только для объектов классов ofstream или fstream)  
- __ios::app__ – для дозаписи; прежние данные не удаляются  
- __ios::ate__ – при открытии указатель файла смещается в конец  
- __ios::binary__ – открытие файла в бинарном режиме доступа

```C++
#include <iostream>
#include <fstream>

int main(void)
{
    std::ofstream ofs("ofs.dat");
    std::ifstream ifs("ifs.dat", ios::app);

    std::cout << (ofs.is_open() ? "Файл открыт" : "Файл не открыт") << std::endl;
    std::cout << (ifs.is_open() ? "Файл открыт" : "Файл не открыт") << std::endl;

    ofs.close();
    ifs.close();

    return 0;
}
```

Для объединения флагов открытия можно использовать операцию побитового ИЛИ:

```C++
std::ifstream ifs("ifs.dat", ios::app | ios::binary);  // дозапись в байтовом режиме
```

## Чтение и запись данных в файл в текстовом режиме

`std::cout` и `std::cin` по природе своей очень схожи с файловыми потоками. Потому работа с файловыми потоками идентична работе с этими объектами. См. на примерах:

```C++
#include <iostream>
#include <fstream>
#include <string>

int main(void)
{
    std::ofstream ofs("out_course.dat");
    std::string str;

    if(ofs.is_open())
    {
        ofs << 10 << " " << -5.34 << " " << -34 << std::endl;  // запись в файл
        ofs << "Hello World!" << std::endl;  // запись строки в файл
    }

    ofs.close();

    // чтение данных

    int data_i1 {}, data_i2 {};
    double data_d1 {};

    std::ifstream ifs("out_course.dat");

    if(ifs.is_open())
    {
        ifs >> data_i1 >> data_d1 >> data_i2;  // чтение из файла
//        ifs >> str;  // чтение строки до пробельного символа
//        getline(ifs, str);  // чтение строки целиком, сейчас курсор указывает на символ переноса строки ,поэтому str будет пустой строкой
        while(str.length() == 0 && !ifs.eof())
            getline(ifs, str);
    }
    ifs.close();

    std::cout << data_i1 << " " << data_i2 << " " << data_d1 << std::endl;
    std::cout << str << std::endl;
    return 0;
}
```

Метод `ifs.eof()` возвращает истину, когда мы доходим до конца файла.

## Чтение и запись данных в файл в бинарном режиме

```C++
#include <iostream>
#include <fstream>

using std::ios;

int main(void)
{
    double pow[] {4.3, -5.4, 0.01, 7.88};

    std::ofstream ofs("out_course.dat", ios::out | ios::binary);
    
    if(ofs.is_open()) {
        ofs.write((char *)pow, sizeof(pow));
    }

    ofs.close();

    // чтение данных из файла

    double read_pow[5] {0};
    std::ifstream ifs("out_course.dat", ios::in | ios::binary);

    if(ifs.is_open()) {
        ifs.read((char *)read_pow, sizeof(pow));
    }

    for(double x : read_pow)
        std::cout << x << ' ';
    return 0;
}
```

Для бинарной записи данных в файл необходимо воспользоваться методом `.write()` у объекта файлового потока. Этому методу в качестве аргумента необходимо передать байтовый указатель на данные и количество читаемых байтов.

Для бинарного чтения данных из файла необходимо воспользоваться методом `.read()` у объекта файлового потока. Этому методу в качестве аргумента необходимо передать байтовый указатель на ячейки памяти, в которые будем записывать данные из файла и количество читаемых байтов.

## Перегрузка функций. Директива extern C

```C++
#include <iostream>

int module_int (int x)
{
    std::cout << "module_int(int)" << std::endl;
    if(x >= -10 && x <= 10)
        return (x > 0) ? x : -x;
    return x;
}

double module_double (double x)
{
    std::cout << "module_double(double)" << std::endl;
    if(x >= -10 && x <= 10)
        return (x > 0) ? x : -x;
    return x;
}

int main(void)
{
    int x = -10;
    int res = module_int(x);
    std::cout << res << std::endl;

    return 0;
}
```

Тут есть неудобство, что, хоть функции делают одно и то же, программисту нужно задумываться, какую из них вызвать? Однако, язык C++ позволяет определять функции с одинаковыми названиями, но разными типами входных и выходных данных:

```C++
#include <iostream>

int module (int x)
{
    std::cout << "module_int(int)" << std::endl;
    if(x >= -10 && x <= 10)
        return (x > 0) ? x : -x;
    return x;
}

double module (double x)
{
    std::cout << "module_double(double)" << std::endl;
    if(x >= -10 && x <= 10)
        return (x > 0) ? x : -x;
    return x;
}

int main(void)
{
    int x = -10;
    int res1 = module(x);
    std::cout << res1 << std::endl;

    double res2 = module(-2.0);
    std::cout << res2 << std::endl;
    return 0;
}
```

Теперь компилятор сам будет понимать, какую реализацию исполнять в соответствии с типами получаемых параметров, а ожидаемые типы данных не играют абсолютно никакой роли

Такая перегрузка функций относится к статическому полиморфизму.

Тут получается проблема с перегрузкой, потому что до этого линкер на этапе сборки объектных файлов искал реализации функций по уникальной метке <название функции>. Теперь этого мало и ему нужно найти уникальную метку <_Z<кол-во символов в имени функции><имя функции><типы параметров>>. Разные компиляторы справляются с задачей кодировки уникальной метки по-разному, и потому, могут возникать проблемы. Это происходит не просто у разных компиляторов, а даже у разных версий одного и того же компилятора, что уж говорить о коде, написанном на C, который планируется использовать на C++. Именно для этих целей, объявление функций в коде C++ необходимо поместить в директиву `extern "C" {}` (в том случае, если функции были скомпилированы на языке C). Естественно в этой директиве нельзя определять перегруженные функции. Эта директива существует в C++, но не существует в C. Эту проблему можно решить с помощью директив условной компиляции:

```C++
#include <iostream>

#ifdef __cplusplus
extern "C" {
#endif
void show_msg(const char* msg)
{
    ...
}
#ifdef __cplusplus
}
#endif
```

## Значения параметров функции по умолчанию

```C++
#include <iostream>

void show_data(int a=1, const char* str="Hi!", double b=-5.43)
{
    std::cout << a << ' ' << str << ' ' << b << std::endl;
}

int main(void)
{
    show_data();
    show_data(2);
    show_data(3, "Hello, World");
    show_data(5, "H", -2.0);
    return 0;
}
```

Параметры со значениями по умолчанию должны следовать обязательно после обыкновенных позиционных.

## inline-функции

Так называемые, отставляемые функции. В случае, если мы пользуемся достаточно простыми функциями, буквально в одну строчку, то компилятору неразумно вызывать такую функцию, нагружать а позже разгружать стековый фрейм. В основном компиляторы на данных этапах подставляют реализацию таких функций в машинный код обходя вызов функции и нагрузку на стековый фрейм. Если программист понимает, что такая операция ускорит выполнение кода программы, он может прописать ключевое слово `inline` перед заголовком функции. После этого на уровне машинных кодов вместо вызовов такой функции будет подставляться ее реализация.

```C++
#include <iostream>
#include <math.h>

inline bool sqr_root(double a, double b, double c, double& x1, double& x2)
{
    double D = b*b - 4 * a * c;
    if (D < 0) return false;

    x1 = -(b + sqrt(D)) / (2*a);
    x2 = -(b - sqrt(D)) / (2*a);
    return true;
}


int main()
{
    double x1{}, x2 {};

    bool res_root = sqr_root(3, 10, 5, x1, x2);
    if(res_root)
        std::cout << x1 << ' ' << x2 << std::endl;

    return 0;
}
```

## Лямбда-функции (анонимные функции)

Лямбда-выражения позволяют создавать простой объект-функцию в любом допустимом месте программы. Одно из таких мест - аргумент обычной функции. Синтаксис:

```markdown
[] ([параметры]) {<операторы тела функции>}
```

В этом определении отсутствует имя функции.

```C++
#include <iostream>

int main()
{
    [] (int a) {
        std::cout << "Lambda function: " << a << std::endl;
    }(10);  // вызов функции после ее определения

    auto r = [] (int a) {  // определение имени объекта-функции
        std::cout << "Lambda function: " << a << std::endl;
    };

    r(10);  // r - не ссылается на лямбда-функцию, а само ей является

    auto s = r;  // при этом s - это еще один объект функции и оно не ссылается ни на что
    s(15);
    return 0;
}
```

Тип такого объекта, который [тип] формируется автоматически - это обычная функция. Чтобы указать тип возвращаемых данных, нужно прописать стрелочку:

```C++
    auto r = [] (int a) -> double {  // определение имени объекта-функции
        std::cout << "Lambda function: " << a << std::endl;
    };
```

Начиная с C++14 в параметрах лямбда-выражения можно определять вычисляемых тип данных:

```C++
#include <iostream>

int main()
{
    auto sum2 { [] (auto a, auto b) -> auto {return a+b;} };

    std::cout << sum2(2, 3) << std::endl;

    double res_1 = sum2(2, 3);
    double res_2 = sum2(2.4, 3.5);

    std::cout << res_1 << " " << res_2 << std::endl;

    return 0;
}
```

Также можно поступать и со строками:

```C++
#include <iostream>
#include <string>

int main()
{
    auto sum2 { [] (auto a, auto b) -> auto {return a+b;} };

    std::cout << sum2(2, 3) << std::endl;

    double res_1 = sum2(2, 3);
    double res_2 = sum2(2.4, 3.5);
    std::string res_3 = sum2(std::string("Hello"), std::string(" world!"));

    std::cout << res_1 << " " << res_2 << " " << res_3 << std::endl;

    return 0;
}
```

Приведем пример, где лямбда-выражения применять очень удобно:

```C++
#include <iostream>

void show_ar(const int* ar, size_t length, bool (*filter_func)(int) = nullptr)
{
    for(int i = 0; i < length; ++i) {
        if(filter_func != nullptr) {
            if(!filter_func(ar[i])) continue;
        } else {
            std::cout << ar[i] << ' ';
        }
    }
    std::cout << std::endl;
}

int main()
{
    int data[] {1, 2, 3, 4, 5, 6, 7, 8};
    show_ar(data, sizeof(data)/sizeof(*data));

    return 0;
}
```

## Захват внешних значений в лямбда выражениях

Для чего же нужны и как используются квадратные скобки, стоящие перед каждым лямбда-выражением?

Через них можно передавать различные переменные из внешней области видимости, тогда как глобальные переменные доступны в таких функциях априори. Этот процесс в C++ называется __захват переменных__.


```C++
#include <iostream>

const int max_size = 1000;

int main()
{
    int sz = 10;

    auto r = [] () {
        std::cout << max_size << std::endl;   // нет ошибки 
        std::cout << sz << std::endl;         // есть ошибка
    };

    r();

    return 0;
}
```

Символ `=` внутри квадратных скобок будет означать, что внутри локальной области видимости лямбда-выражения будут доступны те же переменные, но есть одно "но". Значения этих переменных будут скопированы и присвоены константным переменным внутри лямбда-выражений

Также, существует ключевое слово `mutable`, которое можно поставить после круглых скобок для того, чтобы переменные внутри лямбда-выражений были не постоянные, а обычные.

Вместо символа `=` можно указать напрямую, какие переменные из внешней области видимости необходимо захватить.

```C++
#include <iostream>

const int max_size = 1000;

int main()
{
    int sz = 10;

    auto r = [sz] () mutable {
        ++sz;
        std::cout << max_size << std::endl;
        std::cout << sz << std::endl;
    };

    r();

    return 0;
}
```

Символ `&` внутри квадратных скобок лямбда-выражений означает передачу переменных из внешней области видимости по ссылкам (тогда `mutable` можно опустить):

```C++
#include <iostream>

int main()
{
    int sz = 10;

    auto r = [&] () mutable {
        ++sz;
    };

    std::cout << sz << std::endl;
    r();
    std::cout << sz << std::endl;

    return 0;
}
```

Не все переменные, а отдельные можно передавать по ссылке таким образом:

```C++
auto r = [&n1, &n2] () {return 0;};
```

Хоть по указателям менять данные можно, по указателям на массивы, элементы этих массивов ~~почему-то~~ изменяться не будут:

```C++
#include <iostream>

int main()
{
    int ar[] = {1, 2, 3, 4, 5, 6, 7, 8};
    size_t size = sizeof(ar) / sizeof(*ar);
    auto r = [ar, size] () mutable {
        for(int i = 0; i < 2; ++i) {
            ar[i] *= 2;
        }
        for(int i = 0; i < size; ++i) {
            std::cout << ar[i] << ' ';
        }
        std::cout << std::endl;
    };

    r();

    for(int x : ar)
        std::cout << x << ' ';
    std::cout << std::endl;

    return 0;
}
```

# Структуры в C++. Работа с памятью

## Структуры в С++, как обновленный тип данных

Структуры в языке C++ преобразились и стали, фактически, классами

В C и C++ структуры объявляются одинаково, но в отличии от C , в плюсах структуры являются отдельными типами данных:

```C++
#include <iostream>

struct point {int x, y;};

int main ()
{
    point pt1 {};    // pt_1.x = 0, pt_1.y = 0
    point pt_2 {1};  // pt_2.x = 1, pt_2.y = 0

    std::cout << pt_2.x << ' ' << pt_2.y << std::endl;
    return 0;
}
```

Также, прямо в структуре можно объявлять функции, такие функции называются __функции-члены__, или просто __методы__:

```C++
#include <iostream>
#include <math.h>

struct point {
    int x, y;
    
    double length() {return sqrt(x*x + y*y);};
};

int main ()
{
    point pt1 {};    // pt_1.x = 0, pt_1.y = 0
    point pt_2 {1};  // pt_2.x = 1, pt_2.y = 0

    std::cout << pt_2.x << ' ' << pt_2.y << std::endl;
    std::cout << pt_2.length() << std::endl;

    return 0;
}
```

У методов есть прямой доступ к атрибутам структуры, для которой мы применяем метод. Откуда же у них такой доступ? На самом деле, при вызове метода скрытно передается в тело метода специальный неявный указатель `this` (аналог `self` в Python) на объект структуры:

```C++
#include <iostream>
#include <math.h>

struct point {
    int x, y;
    
    double length() {return sqrt(this->x*this->x + this->y*this->y);};
};

int main ()
{
    point pt1 {};    // pt_1.x = 0, pt_1.y = 0
    point pt_2 {1};  // pt_2.x = 1, pt_2.y = 0

    std::cout << pt_2.x << ' ' << pt_2.y << std::endl;
    std::cout << pt_2.length() << std::endl;

    return 0;
}
```

Указатель `this` всегда имеет тип: указатель на текущую структуру.

Указатель `this` не передается в статические методы:

```C++
struct point {
    int x, y;

//    static void show_coords() {std::cout << this->x << ' ' << this->y << std::endl;};  // ошибка!
    void show_coords() {std::cout << this->x << ' ' << this->y << std::endl;};
}
```

## Структуры. Режимы доступа. Сеттеры и геттеры

Значения полей структуры можно менять через простое обращение оператором `.`:

```C++
pt.x = 10;
pt.y = 20;
```

Это не является желаемым поведением в структуре объектно-ориентированного программирования, т.к. может нести непредсказуемое программисту поведение программы. Как же быть с этим? В структурах существуют типы доступа. Мы рассмотрим два из них:

* __public__ - общий;
* __private__ - частный.

Данные типы доступа работают по принципу меток (например, ниже всё, что попадает под метку `private`, будет считаться приватным. Метка считается до следующей метки либо до конца тела структуры):

```C++
struct point {
private:
    int x, y;
public:
    double length() {return sqrt(x*x + y*y);}
}
```

Приватные поля мы не можем инициализировать! Обратите внимание, что внутри публичных методов обращение к приватным переменным __разрешено__

```C++
#include <iostream>
#include <math.h>

struct point {
private:
    int x, y;
public:
    double length() {return sqrt(x*x + y*y);}
};

int main()
{
    struct point pt;
    std::cout << pt.length() << std::endl;

    return 0;
}
```

Очень важная интересная фича заключается в том, что ключевое слово `private` объявляет защиту переменных не на уровне объектов, а на уровне структур целиком. Приведем пример:

```C++
#include <iostream>
#include <math.h>

struct point {
private:
    int x, y;
public:
    double length() {return sqrt(x*x + y*y);}
    void sum(const point& pt)
    {
        this->x += pt.x;  // так можно
        this->y += pt.y;  // так можно
    }
};

int main()
{
    struct point pt;
    std::cout << pt.length() << std::endl;

    return 0;
}
```

Сейчас есть одна проблема: значения приватных переменных непроинициализировано, а значит принимает неопределенное значение. Определим соответствующие публичные методы:

```C++
#include <iostream>
#include <math.h>

struct point {
private:
    int x, y;
public:
    double length() {return sqrt(x*x + y*y);}
    void sum(const point& pt)
    {
        this->x += pt.x;  // так можно
        this->y += pt.y;  // так можно
    }

    void set_coords(int x, int y)
    {
        if(x < -100 || x > 100 || y < -100 || y > 100)
            return;
        
        this->x = x;  // this строго обязательно
        this->y = y;  // this строго обязательно
    }
    void get_coords(int& x, int& y) { x = this->x; y = this->y; }
    int get_x() {return x;}
    int get_y() {return y;}
};

int main()
{
    point pt;

    pt.set_coords(3, 4);
    
    std::cout << pt.length() << std::endl;
    std::cout << pt.get_x() << ' ' << pt.get_y() << std::endl;
    
    int coord1, coord2;
    pt.get_coords(coord1, coord2);

    std::cout << coord1 << ' ' << coord2 << std::endl;

    return 0;
}
```

Методы, которые служат для установки значений полей структур / классов называют __сеттерами__

Методы, которые служат для получения значений полей структур / классов называют __геттерами__

## Структуры. Конструкторы и деструкторы

Конструктор - это специальный метод, который ничего не возвращает, называется так же, как и тип структуры, в которой определяется и вызывается всегда при создании нового объекта.

```C++
#include <iostream>
#include <math.h>

struct point {
private:
    int x, y;
public:
    point()  // конструктор
        { x = 0; y = 0;}

    double length() {return sqrt(x*x + y*y);}
    void sum(const point& pt)
    {
        this->x += pt.x;  // так можно
        this->y += pt.y;  // так можно
    }

    void set_coords(int x, int y)
    {
        if(x < -100 || x > 100 || y < -100 || y > 100)
            return;
        
        this->x = x;  // this строго обязательно
        this->y = y;  // this строго обязательно
    }
    void get_coords(int& x, int& y) { x = this->x; y = this->y; }
    int get_x() {return x;}
    int get_y() {return y;}
};

int main()
{
    point pt;

    // pt.set_coords(3, 4);
    
    std::cout << pt.length() << std::endl;
    std::cout << pt.get_x() << ' ' << pt.get_y() << std::endl;
    
    int coord1, coord2;
    pt.get_coords(coord1, coord2);

    std::cout << coord1 << ' ' << coord2 << std::endl;

    return 0;
}
```

Можно прописать ещё один конструктор с соответствующими параметрами:

```C++
#include <iostream>
#include <math.h>

struct point {
private:
    int x, y;
public:
    point()  // конструктор
        { x = 0; y = 0;}
    point(int x, int y)
        { this->x = x; this->y = y;}

    double length() {return sqrt(x*x + y*y);}
    void sum(const point& pt)
    {
        this->x += pt.x;  // так можно
        this->y += pt.y;  // так можно
    }

    void set_coords(int x, int y)
    {
        if(x < -100 || x > 100 || y < -100 || y > 100)
            return;
        
        this->x = x;  // this строго обязательно
        this->y = y;  // this строго обязательно
    }
    void get_coords(int& x, int& y) { x = this->x; y = this->y; }
    int get_x() {return x;}
    int get_y() {return y;}
};

int main()
{
    point pt(1, 2);

    // pt.set_coords(3, 4);
    
    std::cout << pt.length() << std::endl;
    std::cout << pt.get_x() << ' ' << pt.get_y() << std::endl;
    
    int coord1, coord2;
    pt.get_coords(coord1, coord2);

    std::cout << coord1 << ' ' << coord2 << std::endl;

    return 0;
}
```

Таким образом можно перегружать конструкторы

Соответственно метод, который вызывается в момент уничтожения объекта - это __деструктор__. Перед его именем в структуре прописывается знак тильды `~`

```C++
~point()
{
    std::cout << "Уничтожение объекта" << std::endl;
}
```

## Операторы new / delete и new [] / delete []

В связи со всем появившимся функционалом у структур, появились некоторые особенности при работе с памятью, связанной со структурами.

В языке C мы часто пользовались функциями для выделения памяти: `malloc()`, `calloc()`, `realloc()`, `free()`. Используем данный приём в имеющемся коде:

```C++
#include <iostream>
#include <math.h>

struct point {
private:
    int x, y;
public:
    point()  // конструктор
        { x = 0; y = 0;}
    point(int x, int y)
        { this->x = x; this->y = y;}

    double length() {return sqrt(x*x + y*y);}
    void sum(const point& pt)
    {
        this->x += pt.x;  // так можно
        this->y += pt.y;  // так можно
    }

    void set_coords(int x, int y)
    {
        if(x < -100 || x > 100 || y < -100 || y > 100)
            return;
        
        this->x = x;  // this строго обязательно
        this->y = y;  // this строго обязательно
    }
    void get_coords(int& x, int& y) { x = this->x; y = this->y; }
    int get_x() {return x;}
    int get_y() {return y;}
};

int main()
{
    point* pt;
    pt = (point *)malloc(sizeof(point));
    // что-то делаем
    free(pt);

    return 0;
}
```

Но при запуске такой программы не будет выполнен ни конструктор, ни деструктор. В связи с этим были введены операторы `new` и `delete`:

* __new__ - для выделения памяти под указанный тип данных с автоматическим вызовом конструктора;
* __delete__ - освобождение памяти с автоматическим вызовом деструктора.

Функцию `main` тогда изменяем так:

```C++
int main()
{
    point* pt;
    pt = new point;
    delete pt;

    return 0;
}
```

Для использования перегруженного конструктора, можно использовать такой синтаксис:

```C++
pt = new point(10, 20);
```

Тогда будет вызван конструктор, у которого определены два целочисленных параметра.

Такие операторы `new` и `delete` можно использовать и с основными типами данных:

```C++
int main()
{
    int* ptr_int = new int(15);
    delete ptr_int;

    return 0;
}
```

Для того, чтобы создать массив объектов, существуют операторы `new []` и `delete[]`.

* __new []__ - для выделения памяти под указанное число объектов;
* __delete []__ - для освобождения памяти массива объектов.

```C++
// структура pt

int main ()
{
    point* pt = new point[3];

    delete [] pt;

    return 0;
}
```

##  Особенности работы new и delete

У данных операторов, конечно же, есть свои ньюансы:

```C++
#include <iostream>
 
using std::cout;
using std::endl;
 
struct volume {
    // конструктора я не вижу, но он есть
    int width, height, depth;
};

int main(void)
{
    volume* v_1 = new volume;               // поля принимают неопр. значения
    volume* v_2 {new volume};               // эквивалент
    volume* v_3 = new volume();             // все поля инициализируются нулями
    volume* v_4 {new volume{1, 2, 3}};      // согласуется с инициализацией
 
    cout << v_1->width << " " << v_1->height << " " << v_1->depth << endl;
    cout << v_3->width << " " << v_3->height << " " << v_3->depth << endl;
    cout << v_4->width << " " << v_4->height << " " << v_4->depth << endl;
 
    delete v_1;
    delete v_2;
    delete v_3;
    delete v_4;
 
    return 0;
}
```

Аналогичные манипуляции можно производить с обычными типами данных:

```C++
#include <iostream>

int main(void)
{
    int* p1 = new int;
    double* p2 {new double()};
    short* p3 {new short{-5}};
    unsigned p4 {new unsigned(11)};

    std::cout << *p1 << ' ' << *p2 << ' ' << *p3 << ' ' << *p4 << std::endl;

    delete p1;
    delete p2;
    delete p3;
    delete p4;

    return 0;
}
```

Аналогичные манипуляции можно производить с массивами:

```C++
int main(void)
{
    int* ar_1 {new int[7] {}}; // int* ar_1 = new new int[7] {};
    int* ar_2 {new int[4] ()}; // int* ar_2 = new new int[7] ();
    short* ar_3 {new short[11] { 1, 2 }};  // 1, 2, 0, 0
 
    delete ar_1;
    delete ar_2;
    delete ar_3;
 
    return 0;
}
```

Освобождать одну и ту же динамическую память 2 и более раз - нельзя. Поэтому после освобождения памяти, можно освобожденному указателю задавать значение `nullptr`

## Smart-указатели типа unique_ptr

Как уже обсуждалось ранее, Cшные методы выделеления динамической памяти в C++ уже попросту не являются безопасными. Потому в практике программирования встречаются такие возможные ошибки:

* Выделенная, но не освобождённая память (утечка памяти).
* Память освобождена, но продолжает использоваться (висячий указатель).
* Запись данных в память, которая не была выделена.
* Попытка несколько раз освободить одну и ту же область памяти.

Спрашивается, как тогда минимизировать шанс ошибки? В высокоуровневых языках программирования (Java, Python, C#) предусмотрен механизм сборки мусора, который отслеживает неиспользуемую память и автоматически её освобождает. Но в C++ нет такого сборщика. Несмотря на это, решение все же есть - это использование `smart-`указателей.

* __unique_ptr__ - уникальный (в единственном числе) smart-указатель, ссылающийся на выделенную область памяти (или принимающий значение `nullptr`);
* __shared_ptr__ - smart-указатель, допускающий множественные адресации на одну и ту же выделенную область памяти.

Для использования таких smart-указателей, необходимо подключить файл `<memory>`:

```C++
#include <iostream>
#include <memory>

int main(void)
{
    // ptr_1 = ptr_2 = ptr_3 = nullptr

    std::unique_ptr<int> ptr_1;
    std::unique_ptr<int> ptr_2 {};  // инициализируем указатель
    std::unique_ptr<int> ptr_3 {nullptr};
 
    if(ptr_1)
        std::cout << *ptr << std::endl;

    if(!ptr)
        ptr = std::make_unique<int>(10);  // эта функция выделяет память и записывает туда 10

    *ptr = 7;

    std::cout << *ptr << std::endl;

    return 0;
}
```

Синтаксис unique_ptr: 

```markdown
std::unique_ptr<тип данных, с которым работает указатель> ptr;  ptr - имя указателя
```

Попытаемся выделить память дважды:

```C++
#include <iostream>
#include <memory>

int main(void)
{
    std::unique_ptr<int> ptr_1;

    ptr = std::make_unique<int>(10);
    ptr = std::make_unique<int>(11);

    std::cout << *ptr << std::endl;

    return 0;
}
```

На самом деле тут утечки памяти не происходит! Это происходит именно так, потому что в перегруженном операторе присваивания первоначально происходит процесс освобождения ранее занятой памяти, а уже после присвоение указателя на новую.

Также при штатном завершении функции `main`, умный указатель сам уничтожается, нам не нужно это делать вручную.

Функция `make_unique` появилась относительно недавно: в стандарте C++14. До этого выделялась память при помощи обычного оператора `new`, но так делать крайне не рекоммендуется! И вот почему:

* области памяти, выделяемые на указатель и данные, на который этот указатель ссылается могут располагаться в разных частях программы, что несколько замедляет работу с ними;
* при создании умных указателей в аргументах какой-либо функции оператор `new` и создания самого указателя могут происходить в разные моменты времени. В некоторых случаях такое несогласование может вести к потенциальным ошибкам.

Данные указатели `unique_ptr` ссылаются только на одну область памяти, в частности это означает, что мы не можем одному указателю присвоить значения другого.

Smart-указатель типа `unique_ptr` имеет ряд полезных методов:

- __get()__ — возвращает «сырой» указатель на выделенную область памяти.  
- __release()__ — возвращает указатель на выделенную область памяти и «отвязывает» smart-указатель от неё.  
- __reset()__ — меняет значение указателя на другую область памяти или устанавливает его в `nullptr`, если новый адрес не указан.  
- __swap()__ — выполняет обмен адресами smart-указателей между собой.  

```C++
#include <iostream>
#include <memory>

int main(void)
{
    std::unique_ptr<int> ptr_1 {std::make_unique<int>()};
    std::unique_ptr<int> ptr_2 {};  
    std::unique_ptr<int> ptr_3 {nullptr};

    int* p = ptr_1.get();
    std::cout << p << " " << *p << std::endl;

    return 0;
}
```

```C++
#include <iostream>
#include <memory>

int main(void)
{
    std::unique_ptr<int> ptr_1 {std::make_unique<int>()};
    std::unique_ptr<int> ptr_2 {};  
    std::unique_ptr<int> ptr_3 {nullptr};

    int* p = ptr_1.release();
    std::cout << ptr_1.get() << " " << p << " " << *p << std::endl;

    delete p;  // так будет правильно, т.к. умный указатель забыл про эту память

    return 0;
}
```

```C++
#include <iostream>
#include <memory>

int main(void)
{
    std::unique_ptr<int> ptr_1 {std::make_unique<int>()};
    std::unique_ptr<int> ptr_2 {};  
    std::unique_ptr<int> ptr_3 {nullptr};

    ptr_1.reset(new int(143));
    std::cout << ptr_1.get() << " " << *ptr_1 << std::endl;

    return 0;
}
```

Обратите внимание, что в примере выше исользовать оператор `new` можно, а `std::make_unique<>` уже нельзя.

```C++
#include <iostream>
#include <memory>

int main(void)
{
    std::unique_ptr<int> ptr_1 {std::make_unique<int>()};
    std::unique_ptr<int> ptr_2 {new int {-6}};  
    std::unique_ptr<int> ptr_3 {nullptr};

    ptr_1.swap(ptr_2);
    std::cout << *ptr_1 << " " << *ptr_2 << std::endl;

    return 0;
}
```

Также тут можно использовать такие выкрутасы:

```C++
unsigned total {10};
std::unique_ptr<int[]> ar {std::make_unique<int[]>(total)};  // массив из total элементов
auto ar_2 {std::make_unique<int[]>(7)};  // массив из 7 эл-тов 
std::unique_ptr<int[]> ar_3 {null_ptr};  // массив, ссылающийся на nullptr
```  

## Smart-указатели типа shared_ptr

```C++
#include <iostream>
#include <memory>

int main(void)
{
    std::shared_ptr<int> ptr;
    std::shared_ptr<int> ptr_2 {};
    std::shared_ptr<int> ptr_3 {nullptr};
    std::shared_ptr<int> ptr_4 {ptr};
    std::shared_ptr<int> ptr_5 {std::make_shared<int>(3)};

    ptr_2 = ptr_5;
    *ptr = 10;
    std::cout << ptr_2 << *ptr_2 << std::endl;

    return 0;
}
```

С такими указателями запрещено выполнять выражения адресной арифметики.

При создании `shared_ptr` в области памяти создаются данные, на которые этот указатель ссылается, а также счетчик указателей на эту память. При объявлении нового указателя на эту область, счетчик увеличивается. При смене адресов указателей, ранее ссылающихся на эту область, счетчик уменьшается. При счетчике указателей равным нулю происходит очистка этой памяти.

Взглянем на основные методы умных указателей типа `shared_ptr`:

- __get()__ — получение «сырого» указателя на выделенную область памяти.
- __reset()__ — меняет значение указателя на другую область памяти либо на `nullptr`, если ничего не указано.
- __swap()__ — меняет адреса двух указателей между собой.
- __unique()__ — возвращает `true` (1), если на выделенную область ссылается только один указатель, и `false` (0) в противном случае.
- __use_count()__ — возвращает текущее значение счетчика ссылок (conter) для текущей области памяти.

```C++
#include <iostream>
#include <memory>

int main(void) {
    std::shared_ptr<int> ptr {std::make_shared<int>(3)};
    std::shared_ptr<int> ptr_2 {};
    std::shared_ptr<int> ptr_3 {nullptr};
    std::shared_ptr<int> ptr_4 {ptr};

    int *p = ptr.get();

    std::cout << *p << std::endl;

    return 0;
}
```

```C++
#include <iostream>
#include <memory>

int main(void) {
    std::shared_ptr<int> ptr {std::make_shared<int>(3)};
    std::shared_ptr<int> ptr_2 {ptr};
    std::shared_ptr<int> ptr_3 {nullptr};
    std::shared_ptr<int> ptr_4 {ptr};

    ptr_2.reset(new int[5] {1, 2, 3});
    int *ar = ptr_2.get();

    for(int i = 0; i < 5; ++i)
        std::cout << ar[i] << " ";

    std::cout << std::endl;

    ptr_2.swap(ptr);

    std::cout << *ptr_2 << " " << ptr.use_count() << std::endl;
    std::cout << ptr.unique() << std::endl;

    return 0;
}
```
