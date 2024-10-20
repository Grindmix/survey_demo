# Survey_demo

Небольшой Django проект завернутый в docker compose.
Является примером работы [этого](https://github.com/Grindmix/survey) проекта.

Для запуска достаточно ввести:
```
docker compose up
```

И перейти на http://localhost:8000/survey/ \
Админ панель: http://localhost:8000/admin/ \
В данном примере уже создана учетная запись суперпользователя, логин: admin пароль: admin \
Регистрация новых пользователей, создание опросов и просмотр результата происходит в админ панели.
Посмотреть результаты: /survey/results/{UUID}/
