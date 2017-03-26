./server.py

Command runs notification server, which can be accesed by sending data through netcat to it, or by using ./notyfy.py program


`./notify.py GET`

That command will get all tasks from server


`./notify.py CLEAR`

Will delete all tasks


`./notify.py DEL foo`

Will delete all tasks starting with foo


`./notify.py foobar`

Will add a task named foobar
