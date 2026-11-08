-- ============================================
-- University Training Database
-- JOIN Queries
-- ============================================


-- 1. Students with their course IDs
SELECT
    s.student_id,
    s.full_name,
    e.course_id
FROM students s
INNER JOIN enrollments e
    ON s.student_id = e.student_id;


-- 2. Students with course names
SELECT
    s.student_id,
    s.full_name,
    c.course_name
FROM students s
INNER JOIN enrollments e
    ON s.student_id = e.student_id
INNER JOIN courses c
    ON e.course_id = c.course_id;


-- 3. Students, courses, and instructors
SELECT
    s.full_name AS student_name,
    c.course_name,
    i.full_name AS instructor_name
FROM students s
INNER JOIN enrollments e
    ON s.student_id = e.student_id
INNER JOIN courses c
    ON e.course_id = c.course_id
INNER JOIN instructors i
    ON c.instructor_id = i.instructor_id;


-- 4. Show all students even if they are not enrolled
SELECT
    s.student_id,
    s.full_name,
    e.course_id
FROM students s
LEFT JOIN enrollments e
    ON s.student_id = e.student_id;


-- 5. Students who are not enrolled in any course
SELECT
    s.student_id,
    s.full_name
FROM students s
LEFT JOIN enrollments e
    ON s.student_id = e.student_id
WHERE e.student_id IS NULL;