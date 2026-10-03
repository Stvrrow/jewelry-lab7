var groupmates = [
    {
        "name": "Александр",
        "surname": "Иванов",
        "group": "БВТ2301",
        "marks": [4, 3, 5]
    },
    {
        "name": "Иван",
        "surname": "Петров",
        "group": "БСТ2302",
        "marks": [4, 4, 4]
    },
    {
        "name": "Кирилл",
        "surname": "Смирнов",
        "group": "БВТ2301",
        "marks": [5, 5, 5]
    },
    {
        "name": "Мария",
        "surname": "Кузнецова",
        "group": "БАП2301",
        "marks": [5, 4, 5]
    },
    {
        "name": "Анна",
        "surname": "Соколова",
        "group": "БСТ2302",
        "marks": [3, 4, 3]
    },
    {
        "name": "Дмитрий",
        "surname": "Попов",
        "group": "БВТ2301",
        "marks": [3, 3, 4]
    }
];

console.log(groupmates);

var rpad = function(str, length) {
    // js не поддерживает добавление нужного количества символов
    // справа от строки, т.е. аналога ljust из Python здесь нет
    str = str.toString(); // преобразование в строку
    while (str.length < length)
        str = str + ' '; // добавление пробела в конец строки
    return str; // когда все пробелы добавлены, возвратить строку
};

var printStudents = function(students) {
    console.log(
        rpad("Имя", 15),
        rpad("Фамилия", 15),
        rpad("Группа", 8),
        rpad("Оценки", 20)
    );
    // был выведен заголовок таблицы
    for (var i = 0; i <= students.length - 1; i++) {
        // в цикле выводится каждый экземпляр студента
        console.log(
            rpad(students[i]['name'], 15),
            rpad(students[i]['surname'], 15),
            rpad(students[i]['group'], 8),
            rpad(students[i]['marks'], 20)
        );
    }
    console.log('\n'); // добавляется пустая строка в конце вывода
};

var average = function(marks) {
    var sum = 0;
    for (var i = 0; i < marks.length; i++)
        sum += marks[i];
    return sum / marks.length;
};

// фильтрация студентов по группе
var filterByGroup = function(students, group) {
    return students.filter(function(student) {
        return student.group.toLowerCase() === group.trim().toLowerCase();
    });
};

// фильтрация студентов по среднему баллу: остаются те, у кого средний балл выше заданного
var filterByAverage = function(students, minAverage) {
    return students.filter(function(student) {
        return average(student.marks) > minAverage;
    });
};

printStudents(groupmates);

var group = prompt("Введите группу для фильтрации студентов:", "БВТ2301");
if (group !== null) {
    console.log("Студенты группы " + group + ":");
    printStudents(filterByGroup(groupmates, group));
}

var minAverage = prompt("Введите средний балл для фильтрации студентов:", "4");
if (minAverage !== null) {
    minAverage = parseFloat(minAverage.replace(",", "."));
    if (isNaN(minAverage)) {
        console.log("Средний балл должен быть числом");
    } else {
        console.log("Студенты со средним баллом выше " + minAverage + ":");
        printStudents(filterByAverage(groupmates, minAverage));
    }
}
