Select count(*) from authors as a
join authors_and_publications as ap
	on  a.AUTHOR_ID = ap.AUTHOR_ID
join publications as p
	on p.PUBLICATION_ID = ap.PUBLICATION_ID
join author_html_cvs as ahc
	on ahc.HTML_CV_TEXT like concat('%', p.TITLE, '%')
where p.YEAR = 1970