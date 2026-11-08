-- ============================================
-- University Training Database
-- Basic SQL Queries
-- ============================================


-- 1. Display all students
SELECT *
FROM students;


-- 2. Display selected columns
SELECT
    student_id,
    full_name,
    city
FROM students;


-- 3. Display students from Sanaa
SELECT
    student_id,
    full_name,
    city
FROM students
WHERE city = 'Sanaa';


-- 4. Display assessments with score >= 90
SELECT *
FROM assessments
WHERE score >= 90;


-- 5. Display scores from 80 up to less than 90
SELECT *
FROM assessments
WHERE score >= 80
  AND score < 90;


-- 6. Display students from Sanaa or Dhamar
SELECT *
FROM students
WHERE city = 'Sanaa'
   OR city = 'Dhamar';


-- 7. Sort students alphabetically
SELECT
    student_id,
    full_name,
    city
FROM students
ORDER BY full_name ASC;


-- 8. Sort assessments from highest score to lowest
SELECT *
FROM assessments
ORDER BY score DESC;


-- 9. Count all students
SELECT
    COUNT(*) AS total_students
FROM students;


-- 10. Calculate average score
SELECT
    AVG(score) AS average_score
FROM assessments;


-- 11. Highest score
SELECT
    MAX(score) AS highest_score
FROM assessments;


-- 12. Lowest score
SELECT
    MIN(score) AS lowest_score
FROM assessments;


-- 13. Sum of all scores
SELECT
    SUM(score) AS total_scores
FROM assessments;


-- 14. Average score for each student
SELECT
    student_id,
    AVG(score) AS average_score
FROM assessments
GROUP BY student_id;


-- 15. Average score for each course
SELECT
    course_id,
    AVG(score) AS average_score
FROM assessments
GROUP BY course_id;


-- 16. Number of students in each city
SELECT
    city,
    COUNT(*) AS student_count
FROM students
GROUP BY city;


-- 17. Students whose average score is >= 85
SELECT
    student_id,
    AVG(score) AS average_score
FROM assessments
GROUP BY student_id
HAVING AVG(score) >= 85;