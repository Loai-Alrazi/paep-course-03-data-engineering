-- ============================================
-- University Training Database
-- Analytical Reports
-- ============================================


-- 1. Total number of students
SELECT
    COUNT(*) AS total_students
FROM students;


-- 2. Number of students by city
SELECT
    city,
    COUNT(*) AS total_students
FROM students
GROUP BY city
ORDER BY total_students DESC;


-- 3. Average score per student
SELECT
    student_id,
    AVG(score) AS average_score
FROM assessments
GROUP BY student_id
ORDER BY average_score DESC;


-- 4. Average score per course
SELECT
    course_id,
    AVG(score) AS average_score
FROM assessments
GROUP BY course_id
ORDER BY average_score DESC;


-- 5. Student performance report
-- Student Name + Course Name + Average Score
SELECT
    s.full_name AS student_name,
    c.course_name,
    AVG(a.score) AS average_score
FROM assessments a
INNER JOIN students s
    ON a.student_id = s.student_id
INNER JOIN courses c
    ON a.course_id = c.course_id
GROUP BY
    s.student_id,
    s.full_name,
    c.course_id,
    c.course_name
ORDER BY average_score DESC;


-- 6. Instructor, course, and performance report
SELECT
    i.full_name AS instructor_name,
    c.course_name,
    AVG(a.score) AS average_score
FROM assessments a
INNER JOIN courses c
    ON a.course_id = c.course_id
INNER JOIN instructors i
    ON c.instructor_id = i.instructor_id
GROUP BY
    i.instructor_id,
    i.full_name,
    c.course_id,
    c.course_name
ORDER BY average_score DESC;


-- 7. High-performing students
SELECT
    s.student_id,
    s.full_name,
    AVG(a.score) AS average_score
FROM students s
INNER JOIN assessments a
    ON s.student_id = a.student_id
GROUP BY
    s.student_id,
    s.full_name
HAVING AVG(a.score) >= 85
ORDER BY average_score DESC;


-- 8. Low-performing students
SELECT
    s.student_id,
    s.full_name,
    AVG(a.score) AS average_score
FROM students s
INNER JOIN assessments a
    ON s.student_id = a.student_id
GROUP BY
    s.student_id,
    s.full_name
HAVING AVG(a.score) < 75
ORDER BY average_score ASC;


-- 9. Number of students enrolled in each course
SELECT
    c.course_name,
    COUNT(e.student_id) AS enrolled_students
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id = e.course_id
GROUP BY
    c.course_id,
    c.course_name
ORDER BY enrolled_students DESC;


-- 10. Advanced student performance report
SELECT
    s.student_id,
    s.full_name AS student_name,
    s.city,
    COUNT(DISTINCT e.course_id) AS courses_count,
    AVG(a.score) AS average_score,
    MAX(a.score) AS highest_score,
    MIN(a.score) AS lowest_score
FROM students s
LEFT JOIN enrollments e
    ON s.student_id = e.student_id
LEFT JOIN assessments a
    ON s.student_id = a.student_id
GROUP BY
    s.student_id,
    s.full_name,
    s.city
ORDER BY
    average_score DESC;


SELECT
    s.full_name,
    AVG(a.score) AS average_score
FROM students s
JOIN assessments a
    ON s.student_id = a.student_id
GROUP BY
    s.student_id,
    s.full_name;    