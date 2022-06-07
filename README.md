# 06-Application for parking ticket-machine

#### Introduction:
This project is a DevOps school-project that is divided into two sprints, where I'm responsible for the first and another student from my class will takeover the project for the final sprint. The project itself is a Python and Tkinter based GUI application that simulates a car parking ticket machine. 

#### Project overview:
The concept is about creating a GUI application with Python/Tkinter and use a SQLite database to store related data. The GUI application simulates a car parking ticket machine for a parking lot with 50 parking spots. The parking lot has a pricelist where the ticket itself will be mailed to the ''car driver'' (Mailhog) as a receipt in PDF-format.

The main features of the application are the following:
* Start parking
* See status for parked car
* Stop parking

#### Deeper documentation:
More advanced and detailed documentation about planning, database, sprints, features and todo will be found in the PDF file in the repository. There is also documentation about task tracking for each sprint and feature.
########################################################################
#### Summary overview of continued work after handover of this project.
This project was hand over to me as a part of a project in the Dev.Ops- course at Chas Academy. One student started the project and then another student continued the work. Down below is som screenshots of the continued work done by me, Sara Petré.

Picture 1. Data base in SQLite DB Browser
![](https://i.imgur.com/Po1rYf5.png)

Picture2. Table overview of 'parked_cars'. Look att car BBB222! It has a starting time when parking was started but have not been stoped yet. The stop_time is 'ACTIVE'.
![](https://i.imgur.com/DoXUXjn.png)

Picture3. Start the application and press 'Stop parking'
![](https://i.imgur.com/l29gJpt.png)

Picture 4. A new pop-up window ask the user to add the registration number. Press 'stop parking'.
![](https://i.imgur.com/8OTjMPT.png)

Picture 5. Shows how the parking have now been stopped. A stop_time, calculated total_time parked and price have been added to the table.
![](https://i.imgur.com/7zTvLiP.png)

Picture 6. The summary of the specific car is also shown in the pop-up window. Notice that the same parking time and price is in both the table and the summary.
![](https://i.imgur.com/Y4AnNcC.png)

Picture 7. When pressing the X in the previous pop-up there is a new pop-up window asking the users registration number and email to be able to send the receipt. Press sent-buttom.
![](https://i.imgur.com/nfmIklx.png)

Picture 8. New pop-up with information that the receipt have been sent to MailHog. Press ok!
![](https://i.imgur.com/HrIFMUU.png)

Picture 9. Car info have been removed pop-up window.
![](https://i.imgur.com/j6GM3hI.png)

Picture 10. Show the email added by user into driver table.
![](https://i.imgur.com/tcWUDwj.png)

Picture 11. The car with registrations number BBB222 is removed from table parked_car.
![](https://i.imgur.com/zBewl3o.png)

Picture12. Visiting the localhost 'http://localhost:8025/' show the receipt have been sent by MailHog.
![](https://i.imgur.com/T4bbBHD.png)

Picture 13. The stages are also summarized with short information in the terminal.
![](https://i.imgur.com/gi0xIFT.png)
