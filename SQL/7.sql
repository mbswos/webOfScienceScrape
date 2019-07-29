SELECT count(*) FROM authors as a
join rate_my_professors_professors as rmp
	on a.FIRST_NAME = rmp.TFNAME and a.LAST_NAME = rmp.TLNAME
join rate_my_professors_student_ratings as rs
	on rs.RATE_MY_PROFESSORS_PROFESSOR_ID = rmp.RATE_MY_PROFESSORS_PROFESSOR_ID
	WHERE a.LAST_NAME = 'aboudi'

;
(SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM publications as p
    join UTDallas_publications as up 
        on p.publication_id = up.publication_id
UNION
SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM publications as p
    join journals as j
        on j.journal_name = p.journal
    join financial_times_top_50_journals as ft
        on ft.journal_id = j.journal_id)