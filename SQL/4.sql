Select count(distinct publication_id) from (SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM publications as p
    join UTDallas_publications as up 
        on p.publication_id = up.publication_id
UNION
SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM publications as p
    join journals as j
        on j.journal_name = p.journal
    join financial_times_top_50_journals as ft
        on ft.journal_id = j.journal_id) as qp
	;

Select count(*) from utdallas_publications;
    
SELECT count(p.PUBLICATION_ID) FROM publications as p
    join journals as j
        on j.journal_name = p.journal
    join financial_times_top_50_journals as ft
        on ft.journal_id = j.journal_id