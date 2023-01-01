# erpnext_course1
- We can call this repo as a 3 different projects:
  ## cmd_interact:
    - it is a console prompt program,you can select any option:
      - 1- Register New Student :
        - student name 
        - birth of date
        - Select level (From existing in DB)
        - mobile number
        - email
        
      - 2- Enroll Course:
        - student id
        - course_id
        > **Notes:** 
        > - You have to input the course level same as current student level.
        > 
        > - student can NOT enroll the same course twice.
        > 
        > - student can NOT enroll the course if the capacity is full.
        > 
      - 3- Create New Course:
        - Course Code (Course ID)
        - Course Name 
        - Max Capacity
        - Hour Rate (Price) 
      - 4- Create Course Schedule:
        - Select Day(Weekdays)
        - course_id
        - start time
        - duration
        
        > **Note:** Make sure that there are no any record which has the same course id and the same id at the same slot (start time - end time - day).
          
          
      - 5- Display Student Schedule:
        - student id 
        
    ### How to use:
    - Tested on:
      - `python 3.10.6`
    - Install all required packages for this project by:
      - `$ pip3 install -r requirements.txt`
    - Then you can easily run the cmd interaction script by:
      - `$ python3 cmd`

    
  
    
    
