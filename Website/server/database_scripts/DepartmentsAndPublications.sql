SET SESSION group_concat_max_len = 1000000;
Select d.DEPARTMENT_ID, d.DEPARTMENT_NAME, a.FIRST_NAME, a.LAST_NAME, concat('[',group_concat(concat('{"title":"',replace(p.TITLE,'"','\\"'),'", "year": ', p.YEAR, ', "utdallas":',  IFNULL(u.JOURNAL_ID, 0), ', "ftt50":', IFNULL(j.JOURNAL_ID, 0),'}')),']') as publications from departments as d
	join authors_and_departments as ad on d.DEPARTMENT_ID = ad.DEPARTMENT_ID
    join authors as a on a.AUTHOR_ID = ad.AUTHOR_ID
    left join authors_and_publications as ap on ap.AUTHOR_ID = a.AUTHOR_ID
    left join (select * from publications where publications.year >= 1990) as p on p.PUBLICATION_ID = ap.PUBLICATION_ID
    left join journals as j on j.JOURNAL_NAME = p.JOURNAL
    left join utdallas_journals as u on u.JOURNAL_ID = j.JOURNAL_ID
    left join financial_times_top_50_journals as f on f.JOURNAL_ID = j.JOURNAL_ID
    group by a.author_id
	order by d.DEPARTMENT_ID, a.AUTHOR_ID