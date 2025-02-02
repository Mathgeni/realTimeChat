автор: Канунников Никита
tg: @nikita_kanun

### О проекте:
Данный репозиторий представляет решение масштабирования Websocket
соединений через брокер сообщений

### Контекст:
WebSocket - это технология, разработанная для обеспечения
real-time коммуникации между клиентами и сервером. В отличие
от традиционных HTTP-запросов, WebSocket поддерживает постоянное
и двунаправленное соединение между клиентом и сервером, позволяя
отправлять данные в обе стороны в любой момент. Это существенно 
уменьшает задержки и позволяет создавать более реактивные и быстрые
приложения.

Веб-приложение находящееся в этом репозитории представляет собой
абстрактный чат, клиенты которого могут создавать "чаты" - объединение 
Websocket соединений, в которые отправляются сообщения по мере их 
написания; клиенты могут читатить и писать сообщения в вышеупомянутые
"чаты"

### Проблемы:
1) Каким образом можно масштабировать соединения, по мере возрастания нагрузки?
2) Каким образом доставить сообщение всем клиентам, слушающих один и тот же 
   чат при распределенной нагрузке? 

### Решение проблемы масштабирования:
При решении проблемы горизонтального масштабирования в первую очередь в 
голову приходит идея о прокси сервере, который будет распределять нагрузку 
взависимости от выбранной стратегии. Например: перенаправлять все 
соединения связанные с одним из чатов только в определенный инстанс 
приложения.

Да, действительно эта идея может решить определенный класс проблем, до 
достижения того, что один чат будут слушать столько клиентов, что сервер 
уже не сможет справится с нагрузкой. Как в таком случае уведомлять клиентов?
В таком случае лучшей идеей будет абстрагироваться от конкретных чатов и 
перейти к самим соединениям.

Для простоты понимания WebSocket соединение - это просто-напросто ниточка 
между клиентом и сервером, которая живет на протяжении того, пока либо 
сервер, либо сам клиент не разорвет эту ниточку. 

### Каким образом доставить сообщение всем клиентам, слушающих один и тот же чат при распределенной нагрузке?
Так вот, мы и подошли к самой что ни на есть, основной проблеме: "Как подружить ниточки которые 
находятся на разных инстансах/серверах/VM?". Прошу заметить, что при 
создании WebSocket коннекшена между клиентом и сервером, это соединение 
"живет" только на одном из инстансев приложения, куда перенаправит его 
прокси-сервер, на других инстансах его никак не может существовать. Для 
простоты понимания можно сопоставить это с One-to-One связью в реляционных 
базах данных.

Решение вышеупомянутой проблемы можно решить следующим образом - добавить в 
архитектуру приложения брокер сообщений или очередь сообщений, такой(-ую), что 
при добавление в эту очередь очередного сообщения, отправленного клиентом в 
чат, все слушатели данной очереди смогли его прочтитать и обработать. Тем 
самым, все инстансы приложения, будут слушать одну и ту 
же очередь и одновременно публиковать туда новоотправленные сообщения. Эта 
идея решит проблему отправки сообщений всем клиентам, открывшим соединение 
с опделененным чатом, но она принесла другую - данная очередь является 
узким горлышком системы. Поэтому очередь сообщений нужно выбирать с учетом 
вышеупомянутой проблемы - все consumer`ы слушают одну и ту же очередь. В 
современном мире эта проблема легко решается выбором распределенного 
брокера сообщений, таких как Apache Kafka или других.

### Техническая реализация:
* При открытии WebSocket соединения в приложении будет создан объект 
WebSocketManager, который отвечает за бизнес логику обработки данных 
соединений. Он будет хранить в себе атрибут _connections, который 
представляет собой мапу следующего вида - {chat_id: {user_id: WebSocket}}, 
где WebSocket - объект из пакета websockets. Далее, это соединение будет 
хранится в данном менеджере до его отмены с клиентской или серверной 
стороны или окончанию python процесса. 
* При добавлении нового сообщения в чат, оно в первую очередь сохраняется в 
  базе данных, далее отпавляется в очередь, с другой стороны 
  которой, консьюмер получает это сообщение сопоставляет все WebSocket 
  соединения из вышеупомянутого менеджера и отпавляет им всем полученное сообщение

### Архитектура (Containers):
![Image alt](https://github.com/Mathgeni/realTimeChat/blob/master/chat.drawio.png)