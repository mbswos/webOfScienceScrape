Select * from departments as d
	join authors_and_departments as ad on d.DEPARTMENT_ID = ad.DEPARTMENT_ID
    join authors as a on a.AUTHOR_ID = ad.AUTHOR_ID
    left join google_scholar_author_info as ga on ga.AUTHOR_ID = a.AUTHOR_ID
    order by d.DEPARTMENT_ID, a.AUTHOR_ID