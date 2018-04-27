This is document for anyone who want to run this implementation or test it.
Note: Current version only works on OSX.

-----To install through pip-----
0. assume the git repo path is ./OXT
1. pip3 install ./OXT # it will automatically install some dependencies
2. python3 -c 'import oxt; oxt.run_server()'
3. python3 -c 'import oxt; oxt.run_client()'

-----To set up----
1.Install PyInstaller
2.cd source\ code
3.sh ./gen.sh # it will generate two folder under root path: exe/server and exe/client
4.Open exe/server
5.There is an executable file named server
6.Click it to run server 
7.Open exe/client
8.There is an executable file named client
9.Click it to run client

-----To upload files----
1.Set up and check out to the window for client 
2.Enter "upload"(notice, without any space in the end!)
3.Enter the absolute path of folder you want to upload. (Notice, the formate of files in the folder must be txt. For testing, you can modify files in test folder directly)

=======example ==========
operation>upload
dir> /Users/ningluo/desktop/law2/test
/Users/ningluo/desktop/law2/test
Done sending!


----- To search ---------
(Warn: you can only search after you have uploaded files and don't terminate the program after that)
1.Check out to the the window for client 
2.Enter "search"(notice, without any space in the end!)
3.Enter keywords you want to do conjunctive search, split them with commas(notice, without any space in the end!)
4. Get the result.
=======example ==========
operation>search
keywords>ning,hello
tokens produced...
no such files
operation>search
keywords>ning,and
tokens produced...
result:  {'/Users/ningluo/desktop/law2/test/test.txt', '/Users/ningluo/desktop/law2/test/test3.txt', '/Users/ningluo/desktop/law2/test/test2.txt'}


----- To exit ---------
1.Check out to the the window for client 
2.Enter "exit"(notice, without any space in the end!)

=======example ==========
operation>exit
logout
Saving session...
...copying shared history...
...saving history...truncating history files...
...completed.

[Process completed]
