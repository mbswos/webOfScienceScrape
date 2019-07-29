SELECT IFNULL(teaching_score,0) + IFNULL(publication_score,0), first_name, last_name
FROM
	(SELECT AVG(sr.Roverall) * Tnumratings/(SELECT AVG(TNUMRATINGS) FROM rate_my_professors_professors)
		as teaching_score, p.TLNAME, p.TFNAME from rate_my_professors_professors as p
		join rate_my_professors_student_ratings as sr
			on p.RATE_MY_PROFESSORS_PROFESSOR_ID = sr.RATE_MY_PROFESSORS_PROFESSOR_ID
	group by p.RATE_MY_PROFESSORS_PROFESSOR_ID) as teaching_scores
    
    CROSS JOIN     
	(SELECT 5 * count(pub.PUBLICATION_ID)/(select avg(ct) from (select count(pub.PUBLICATION_ID) as ct
	FROM authors as a
		join authors_and_publications as ap
			on a.AUTHOR_ID = ap.AUTHOR_ID
		join (SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM publications as p
				join UTDallas_publications as up 
					on p.publication_id = up.publication_id
			UNION
			SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM publications as p
				join journals as j
					on j.journal_name = p.journal
				join financial_times_top_50_journals as ft
					on ft.journal_id = j.journal_id) as pub
			on pub.PUBLICATION_ID = ap.PUBLICATION_ID
	group by a.AUTHOR_ID) as qp) as publication_score, a.AUTHOR_ID, a.FIRST_NAME, a.LAST_NAME
	FROM authors as a
		join authors_and_publications as ap
			on a.AUTHOR_ID = ap.AUTHOR_ID
		join (SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM publications as p
				join UTDallas_publications as up 
					on p.publication_id = up.publication_id
			UNION
			SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM publications as p
				join journals as j
					on j.journal_name = p.journal
				join financial_times_top_50_journals as ft
					on ft.journal_id = j.journal_id) as pub
			on pub.PUBLICATION_ID = ap.PUBLICATION_ID
	group by a.AUTHOR_ID) as publication_scores
    on teaching_scores.TFNAME = publication_scores.FIRST_NAME and teaching_scores.TLNAME = publication_scores.LAST_NAME
;
SELECT rating*rating_num + 10*quality_pub_num + cv_pub_num as total_score, rating*rating_num as rate_my_prof_score, quality_pub_num, cv_pub_num, FIRST_NAME, LAST_NAME, AUTHOR_ID
FROM
(SELECT ifnull(avg(sr.ROVERALL),0) as rating, ifnull(rmp.TNUMRATINGS, 0) as rating_num, count(distinct qp.PUBLICATION_ID) as quality_pub_num, count(distinct cvp.PUBLICATION_ID) as cv_pub_num, a.AUTHOR_ID, a.FIRST_NAME, a.LAST_NAME
FROM authors as a
	left outer join authors_and_publications as ap on a.AUTHOR_ID = ap.AUTHOR_ID
    left join (
		SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM publications as p
			join UTDallas_publications as up on p.publication_id = up.publication_id
		UNION
		SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM publications as p
			join journals as j on j.journal_name = p.journal
			join financial_times_top_50_journals as ft on ft.journal_id = j.journal_id
	) as qp on qp.PUBLICATION_ID = ap.PUBLICATION_ID
    left join (
		SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM authors as a
			join authors_and_publications as ap on a.AUTHOR_ID = ap.AUTHOR_ID
			join author_html_cvs as ahc on a.AUTHOR_ID = ahc.AUTHOR_ID
			join publications as p on ap.PUBLICATION_ID = p.PUBLICATION_ID
			where ahc.HTML_CV_TEXT LIKE concat('%', p.TITLE, '%') and p.JOURNAL <> ''
    ) as cvp on cvp.PUBLICATION_ID = ap.PUBLICATION_ID
    left outer join rate_my_professors_professors as rmp on rmp.TFNAME = a.FIRST_NAME and rmp.TLNAME = a.LAST_NAME
    left join rate_my_professors_student_ratings as sr on rmp.RATE_MY_PROFESSORS_PROFESSOR_ID = sr.RATE_MY_PROFESSORS_PROFESSOR_ID
group by a.AUTHOR_ID) as scores
order by total_score desc


        