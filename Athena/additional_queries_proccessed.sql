---Processed---
--All Processed Records
SELECT *
  FROM etl_db.etl_cleaned;

--All Processed Records + Ordered
SELECT *
  FROM etl_db.etl_cleaned
  ORDER BY grade ASC;

--Student Counnt per Grade
SELECT grade, COUNT(name) AS students
FROM etl_db.etl_cleaned
GROUP BY grade 
ORDER BY grade ASC; 

--Lists all unlisted student data and the amount of students with the unlisted entry
Select unlisted, count(name) AS unlisted_count
  From etl.dbetl_cleaned
  Group By unlisted;
