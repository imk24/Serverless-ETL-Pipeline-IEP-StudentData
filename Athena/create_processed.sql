--All Processed Records
SELECT *
  FROM etl_db.etl_cleaned;

--All Processed Records + Ordered
SELECT *
  FROM etl_db.etl_cleaned
  ORDER BY grade ASC;

--Student Counnt per Grade
SELECT grade, COUNT(name) AS students
FROM students
GROUP BY grade 
ORDER BY grade ASC; 
