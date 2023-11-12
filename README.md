# Course management system
## Notes for testing team
1. Class name should start with 'Test'.
2. Testing function name should start with 'test_'
3. Instance creation name should always be SetUp
4. If you are creating any files under tests folder, make sure the filename is starting with test as django looks for test under test folder

5. For running test use python manage.py test Academix_Portal
6. Save the console output in textfile. few sample test case are provided 3 of them are true and one is wrong
   in line 82. 1 != 2 since in line 80, I have added only 1 course i.e Computer Science 101 to faculty aakash.
   (you can read console output sample in model_test.txt)
