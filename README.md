# Численное моделирование уравнения пьезопроводности 

## Описание задачи

В рамках данного расчетного задания выполнено численное моделирование уравнения пьезопроводности для плоско-радиальной задачи с использованием метода конечных разностей (явная схема). В модели учитывается система из двух нагнетательных и двух добывающих скважин, расположенных на расстоянии 1500-2000 метров друг от друга. Задача решается с учетом неоднородности проницаемости пласта, которая может быть задана различными способами.

### Условия задачи:
- **Плоско-радиальная задача**: Рассматривается плоско-радиальная фильтрация флюида в пласте.
- **Система скважин**: 2 нагнетательные и 2 добывающие скважины.
- **Расположение скважин**: Пользовательское задание координат скважин.
- **Расстояние между скважинами**: 1000-2000 метров.
- **Неоднородность пласта**: Проницаемость пласта может быть задана различными способами (квадрат, круг, неровные линии и т.д.).
- **Пласт неограниченный**: Рассматривается неограниченный пласт.

## Структура программы

Программа состоит из нескольких модулей, каждый из которых отвечает за определенную функциональность:

1. **`main.py`**: Основной модуль, который инициализирует параметры задачи, создает объекты скважин, задает начальные условия и запускает процесс решения уравнения пьезопроводности.
2. **`solve.py`**: Модуль, содержащий функции для решения уравнения пьезопроводности методом конечных разностей. Включает в себя функции для применения граничных условий и явного метода решения.
3. **`well.py`**: Модуль, описывающий класс `Well`, который представляет собой скважину с заданными координатами, радиусом, дебитом и другими параметрами.
4. **`results.py`**: Модуль, отвечающий за визуализацию и сохранение результатов моделирования. Включает в себя функции для построения графиков распределения давления, проницаемости, продуктивности скважин, а также создания GIF-анимации.
5. **`Permeability.py`**: Модуль, отвечающий за генерацию матрицы проницаемости пласта с учетом различных типов неоднородности.

## Использование программы

### Задание параметров

1. **Размещение и дебиты скважин**:
   - В модуле `main.py` в переменной `wells` задаются параметры каждой скважины: координаты `x_w` и `y_w`, радиус `r_w`, дебит `q` и номер скважины `number`.
   - Пример:
     ```python
     wells = [
         Well(525, 410, 1.5, 1100, 1),
         Well(2000, 500, 1.5, -1000, 2),
         Well(600, 1800, 1.5, -1000, 3),
         Well(2250, 2200, 1.5, 1000, 4),
     ]
     ```

2. **Расчетный период**:
   - Время работы модели задается в переменной `T` в модуле `main.py`.
   - Пример:
     ```python
     T = 365 * 2  # время работы в сутках
     ```

3. **Вид матрицы проницаемости**:
   - Тип неоднородности проницаемости задается в переменной `type_number` в функции `generate_permeability_matrix` в модуле `Permeability.py`.
   - Пример:
     ```python
     permeability_matrix = Permeability.generate_permeability_matrix(X, Y, permeability, 3)
     ```
   - Доступные типы неоднородности:
     - 1: Квадрат
     ![проницаемость 1.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D0%B4%D0%BB%D1%8F%20%D0%BE%D1%82%D1%87%D0%B5%D1%82%D0%B0%2F%D0%BF%D1%80%D0%BE%D0%BD%D0%B8%D1%86%D0%B0%D0%B5%D0%BC%D0%BE%D1%81%D1%82%D1%8C%201.png)
     - 2: Круг
     ![проницаемость 2.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D0%B4%D0%BB%D1%8F%20%D0%BE%D1%82%D1%87%D0%B5%D1%82%D0%B0%2F%D0%BF%D1%80%D0%BE%D0%BD%D0%B8%D1%86%D0%B0%D0%B5%D0%BC%D0%BE%D1%81%D1%82%D1%8C%202.png)
     - 3: Неровное что-то
     ![проницаемость 3.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D0%B4%D0%BB%D1%8F%20%D0%BE%D1%82%D1%87%D0%B5%D1%82%D0%B0%2F%D0%BF%D1%80%D0%BE%D0%BD%D0%B8%D1%86%D0%B0%D0%B5%D0%BC%D0%BE%D1%81%D1%82%D1%8C%203.png)
     - 4: Линия неровная
     ![проницаемость 4.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D0%B4%D0%BB%D1%8F%20%D0%BE%D1%82%D1%87%D0%B5%D1%82%D0%B0%2F%D0%BF%D1%80%D0%BE%D0%BD%D0%B8%D1%86%D0%B0%D0%B5%D0%BC%D0%BE%D1%81%D1%82%D1%8C%204.png)
     - 5: Линия синус
     ![проницаемость 5.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D0%B4%D0%BB%D1%8F%20%D0%BE%D1%82%D1%87%D0%B5%D1%82%D0%B0%2F%D0%BF%D1%80%D0%BE%D0%BD%D0%B8%D1%86%D0%B0%D0%B5%D0%BC%D0%BE%D1%81%D1%82%D1%8C%205.png)
     - 6: Рандомное
     ![проницаемость 6.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D0%B4%D0%BB%D1%8F%20%D0%BE%D1%82%D1%87%D0%B5%D1%82%D0%B0%2F%D0%BF%D1%80%D0%BE%D0%BD%D0%B8%D1%86%D0%B0%D0%B5%D0%BC%D0%BE%D1%81%D1%82%D1%8C%206.png)
     - 7: Половинка
     ![проницаемость 7.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D0%B4%D0%BB%D1%8F%20%D0%BE%D1%82%D1%87%D0%B5%D1%82%D0%B0%2F%D0%BF%D1%80%D0%BE%D0%BD%D0%B8%D1%86%D0%B0%D0%B5%D0%BC%D0%BE%D1%81%D1%82%D1%8C%207.png)
### Запуск программы

1. Установите необходимые библиотеки:
   ```bash
   pip install numpy torch matplotlib pandas imageio
   ```

2. Запустите основной модуль `main.py`:
   ```bash
   python main.py
   ```

### Результаты

После запуска программы будут созданы следующие файлы:

1. **Графики**:
   - `проницаемость.png`: Распределение проницаемости пласта.
   - `результат_давление.png`: Итоговое распределение давления в пласте.
   - `давление_забой.png`: Давление на забоях скважин в зависимости от времени.
   - `продуктивность.png`: Продуктивность добывающих скважин.

2. **GIF-анимация**:
   - `pressure_evolution.gif`: Эволюция распределения давления в пласте с течением времени.

3. **Excel-файл**:
   - `well_information.xlsx`: Информация о продуктивности и давлении на забоях скважин.

## Пример расчета

В качестве примера расчета используются следующие данные:

- **Скважины**:
  - Скважина 1: `(525, 410)`, дебит `1100 м3/сут`
  - Скважина 2: `(2000, 500)`, дебит `-1000 м3/сут`
  - Скважина 3: `(600, 1800)`, дебит `-1000 м3/сут`
  - Скважина 4: `(2250, 2200)`, дебит `1000 м3/сут`

- **Параметры пласта**:
  - Проницаемость: `1 * 10e-14 м2`
  - Вязкость: `10 * 10e-7 Бар * сут`
  - Сжимаемость: `5 * 10e-5 1/Бар`
  - Пористость: `0.05`

- **Расчетный период**: `2 года`


## Визуализация результатов

### Картинки

1. **Распределение проницаемости**:

![проницаемость.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D0%BF%D1%80%D0%BE%D0%BD%D0%B8%D1%86%D0%B0%D0%B5%D0%BC%D0%BE%D1%81%D1%82%D1%8C.png)
2. **Итоговое распределение давления**:
   ![результат_давление.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D1%80%D0%B5%D0%B7%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1%82_%D0%B4%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5.png)
3. **Давление на забоях скважин**:
   ![давление_забой.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D0%B4%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_%D0%B7%D0%B0%D0%B1%D0%BE%D0%B9.png)
4. **Продуктивность добывающих скважин**:
   ![продуктивность.png](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2F%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D0%BE%D1%81%D1%82%D1%8C.png)
### GIF-анимация
![pressure_evolution.gif](%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7%20%D0%A0%D0%B5%D1%81%D1%87%D0%B5%D1%82%D0%BA%D0%B0%2Fresults%20files%2Fpressure_evolution.gif)


              Эволюция распределения давления



## Зависимости

Программа использует следующие библиотеки:

- `numpy`
- `torch`
- `matplotlib`
- `pandas`
- `imageio`

Убедитесь, что все необходимые библиотеки установлены перед запуском программы.

