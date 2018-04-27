This is document for anyone who want to run this implementation or test it.
//address problems 


-----To set up----
1.Open exe
2.Open server
3.There is an executable file named server
4.Click it to run server 
5.Return back to exe 
6.Open client
7.There is an executable file named client
8.Click it to run client

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
