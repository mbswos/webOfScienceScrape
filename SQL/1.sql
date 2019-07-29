SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM authors as a
	join authors_and_publications as ap on a.AUTHOR_ID = ap.AUTHOR_ID
    join author_html_cvs as ahc on a.AUTHOR_ID = ahc.AUTHOR_ID
    join publications as p on ap.PUBLICATION_ID = p.PUBLICATION_ID
    where ahc.HTML_CV_TEXT LIKE concat('%', p.TITLE, '%') and p.JOURNAL <> ''