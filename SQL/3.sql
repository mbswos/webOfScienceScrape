SELECT p.TITLE, group_concat(a.FULL_AUTHOR_NAME separator ', ') as AUTHORS, p.JOURNAL, p.VOLUME, p.ISSUE, p.YEAR, p.PAGES FROM web_of_science_raw_publications as p
join web_of_science_raw_authors as a on a.WOS_RAW_PUBLICATION_ID = p.WOS_RAW_PUBLICATION_ID 
join authors as au on a.FULL_AUTHOR_NAME LIKE concat('%', au.LAST_NAME, '%')
where YEAR = 2018
group by p.TITLE;