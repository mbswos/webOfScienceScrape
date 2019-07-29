select count(distinct p.PUBLICATION_ID) from authors as a
join authors_and_publications as ap
on ap.AUTHOR_ID = a.AUTHOR_ID
join publications as p
on ap.PUBLICATION_ID = p.PUBLICATION_ID
join google_scholar_publication_info as gsp
on gsp.PUBLICATION_ID = p.PUBLICATION_ID
join author_html_cvs as ahc
on ahc.AUTHOR_ID = a.AUTHOR_ID
where ahc.HTML_CV_TEXT like concat('%', p.TITLE, '%')