---Raw---
--All raw records
SELECT *
  FROM raw_example
  ORDER BY grade ASC;

--Grouping all records by role and grade, counts how many entrys per given role
SELECT role, grade, COUNT(role) AS Amount 
  FROM raw_data 
  GROUP BY role, grade 
  Order BY grade;

--Groups student records by grade, counts how many entrys per grade
SELECT grade, COUNT(role) AS student_count
  FROM raw_data
  WHERE role LIKE "%Stud%"
  GROUP BY grade
  ORDER BY grade;

--Groups teacher records by grade, ounts how many entrys per grade
SELECT grade, COUNT(role) AS teacher_count
  FROM raw_data
  WHERE role LIKE "%Teach%"
  GROUP BY grade  
  ORDER BY grade;

--Groups all grades and classes displays the count for each student with same classes
SELECT grade, class 
  FROM raw_data
  GROUP BY grade, class
  ORDER BY grade;

--Groups all classses and displays all occurences across all grades
SELECT
    class,
    COUNT(*) AS occurrences
  FROM raw_data
  GROUP BY class
  ORDER BY occurrences DESC;
