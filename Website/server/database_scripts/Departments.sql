Select d.DEPARTMENT_ID, d.DEPARTMENT_NAME, count(distinct p.PUBLICATION_ID) as publication_count from departments as d
	join authors_and_departments as ad on d.DEPARTMENT_ID = ad.DEPARTMENT_ID
    join authors as a on a.AUTHOR_ID = ad.AUTHOR_ID
    join authors_and_publications as ap on ap.AUTHOR_ID = a.AUTHOR_ID
    join publications as p on p.PUBLICATION_ID = ap.PUBLICATION_ID
    group by d.DEPARTMENT_ID