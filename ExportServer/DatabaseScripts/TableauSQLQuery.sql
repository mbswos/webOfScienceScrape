SELECT `authors+`.`AUTHOR_ID` AS `AUTHOR_ID`,
  `authors+`.`FIRST_NAME` AS `FIRST_NAME`,
  `authors+`.`MIDDLE_NAME` AS `MIDDLE_NAME`,
  `authors+`.`LAST_NAME` AS `LAST_NAME`,
  `authors+`.`TITLE` AS `TITLE`,
  `authors+`.`SUFFIX` AS `SUFFIX`,
  `authors+`.`NICKNAME` AS `NICKNAME`,
  'authors' AS `Table Name`,
  `authors_and_publications`.`PUBLICATION_ID` AS `PUBLICATION_ID`,
  `rate_my_professors_professors`.`RATE_MY_PROFESSORS_PROFESSOR_ID` AS `RATE_MY_PROFESSORS_PROFESSOR_ID`,
  `rate_my_professors_professors`.`TDEPT` AS `TDEPT`,
  `rate_my_professors_professors`.`TSID` AS `TSID`,
  `rate_my_professors_professors`.`INSTITUTION_NAME` AS `INSTITUTION_NAME`,
  `rate_my_professors_professors`.`TFNAME` AS `TFNAME`,
  `rate_my_professors_professors`.`TMIDDLENAME` AS `TMIDDLENAME`,
  `rate_my_professors_professors`.`TLNAME` AS `TLNAME`,
  `rate_my_professors_professors`.`TID` AS `TID`,
  `rate_my_professors_professors`.`TNUMRATINGS` AS `TNUMRATINGS`,
  `rate_my_professors_professors`.`RATING_CLASS` AS `RATING_CLASS`,
  `rate_my_professors_professors`.`CONTENTTYPE` AS `CONTENTTYPE`,
  `rate_my_professors_professors`.`CATEGORYTYPE` AS `CATEGORYTYPE`,
  `rate_my_professors_professors`.`OVERALL_RATING` AS `OVERALL_RATING`,
  `rate_my_professors_student_ratings`.`RATE_MY_PROFESSORS_STUDENT_RATING_ID` AS `RATE_MY_PROFESSORS_STUDENT_RATING_ID`,
  `rate_my_professors_student_ratings`.`RATE_MY_PROFESSORS_PROFESSOR_ID` AS `RATE_MY_PROFESSORS_PROFESSOR_ID (rate_my_professors_student_ra`,
  `rate_my_professors_student_ratings`.`ATTENDANCE` AS `ATTENDANCE`,
  `rate_my_professors_student_ratings`.`CLARITYCOLOR` AS `CLARITYCOLOR`,
  `rate_my_professors_student_ratings`.`EASYCOLOR` AS `EASYCOLOR`,
  `rate_my_professors_student_ratings`.`HELPCOLOR` AS `HELPCOLOR`,
  `rate_my_professors_student_ratings`.`HELPCOUNT` AS `HELPCOUNT`,
  `rate_my_professors_student_ratings`.`ID` AS `ID`,
  `rate_my_professors_student_ratings`.`NOTHELPCOUNT` AS `NOTHELPCOUNT`,
  `rate_my_professors_student_ratings`.`ONLINECLASS` AS `ONLINECLASS`,
  `rate_my_professors_student_ratings`.`QUALITY` AS `QUALITY`,
  `rate_my_professors_student_ratings`.`RCLARITY` AS `RCLARITY`,
  `rate_my_professors_student_ratings`.`RCLASS` AS `RCLASS`,
  `rate_my_professors_student_ratings`.`RCOMMENTS` AS `RCOMMENTS`,
  `rate_my_professors_student_ratings`.`RDATE` AS `RDATE`,
  `rate_my_professors_student_ratings`.`REASY` AS `REASY`,
  `rate_my_professors_student_ratings`.`REASYSTRING` AS `REASYSTRING`,
  `rate_my_professors_student_ratings`.`RERRORMSG` AS `RERRORMSG`,
  `rate_my_professors_student_ratings`.`RHELPFUL` AS `RHELPFUL`,
  `rate_my_professors_student_ratings`.`RINTEREST` AS `RINTEREST`,
  `rate_my_professors_student_ratings`.`ROVERALL` AS `ROVERALL`,
  `rate_my_professors_student_ratings`.`ROVERALLSTRING` AS `ROVERALLSTRING`,
  `rate_my_professors_student_ratings`.`RSTATUS` AS `RSTATUS`,
  `rate_my_professors_student_ratings`.`RTEXTBOOKUSE` AS `RTEXTBOOKUSE`,
  `rate_my_professors_student_ratings`.`RTIMESTAMP` AS `RTIMESTAMP`,
  `rate_my_professors_student_ratings`.`RWOULDTAKEAGAIN` AS `RWOULDTAKEAGAIN`,
  `rate_my_professors_student_ratings`.`SID` AS `SID`,
  `rate_my_professors_student_ratings`.`TAKENFORCREDIT` AS `TAKENFORCREDIT`,
  `rate_my_professors_student_ratings`.`TEACHERGRADE` AS `TEACHERGRADE`,
  `publications`.`TITLE` AS `TITLE (publications)`,
  `publications`.`JOURNAL` AS `JOURNAL (publications)`,
  `publications`.`YEAR` AS `YEAR (publications)`,
  `publications`.`VOLUME` AS `VOLUME (publications)`,
  `journals`.`JOURNAL_ID` AS `JOURNAL_ID`,
  `journals`.`JOURNAL_NAME` AS `JOURNAL_NAME`,
  `financial_times_top_50_journals`.`JOURNAL_ID` AS `JOURNAL_ID (financial_times_top_50_journals)`,
  `financial_times_top_50_journals`.`JOURNAL_RANK` AS `JOURNAL_RANK`,
  `utdallas_journals`.`DATA_COLLECTION_START_YEAR` AS `DATA_COLLECTION_START_YEAR`,
  `utdallas_journals`.`JOURNAL_URL` AS `JOURNAL_URL`,
  `departments`.`DEPARTMENT_ID` AS `DEPARTMENT_ID (departments)`,
  `departments`.`DEPARTMENT_NAME` AS `DEPARTMENT_NAME`,
  `google_scholar_author_info`.`AFFILIATION` AS `AFFILIATION`,
  `google_scholar_author_info`.`CITEDBY` AS `CITEDBY`,
  `google_scholar_author_info`.`CITEDBY5Y` AS `CITEDBY5Y`,
  `google_scholar_author_info`.`EMAIL` AS `EMAIL`,
  `google_scholar_author_info`.`HINDEX` AS `HINDEX`,
  `google_scholar_author_info`.`HINDEX5Y` AS `HINDEX5Y`,
  `google_scholar_author_info`.`I10INDEX` AS `I10INDEX`,
  `google_scholar_author_info`.`I10INDEX5Y` AS `I10INDEX5Y`,
  `google_scholar_author_info`.`GOOGLE_ID` AS `GOOGLE_ID`,
  `google_scholar_author_info`.`URL_PICTURE` AS `URL_PICTURE`
FROM `authors` `authors+`
  LEFT JOIN `authors_and_publications` ON (`authors+`.`AUTHOR_ID` = `authors_and_publications`.`AUTHOR_ID`)
  LEFT JOIN `rate_my_professors_professors` ON ((`authors+`.`FIRST_NAME` = `rate_my_professors_professors`.`TFNAME`) AND (`authors+`.`LAST_NAME` = `rate_my_professors_professors`.`TLNAME`))
  LEFT JOIN `rate_my_professors_student_ratings` ON (`rate_my_professors_professors`.`RATE_MY_PROFESSORS_PROFESSOR_ID` = `rate_my_professors_student_ratings`.`RATE_MY_PROFESSORS_PROFESSOR_ID`)
  LEFT JOIN `publications` ON (`authors_and_publications`.`PUBLICATION_ID` = `publications`.`PUBLICATION_ID`)
  LEFT JOIN `journals` ON (`publications`.`JOURNAL` = `journals`.`JOURNAL_NAME`)
  LEFT JOIN `financial_times_top_50_journals` ON (`journals`.`JOURNAL_ID` = `financial_times_top_50_journals`.`JOURNAL_ID`)
  LEFT JOIN (
  SELECT p.PUBLICATION_ID, p.JOURNAL, p.TITLE, p.VOLUME, p.YEAR FROM authors as a
  	join authors_and_publications as ap on a.AUTHOR_ID = ap.AUTHOR_ID
      join author_html_cvs as ahc on a.AUTHOR_ID = ahc.AUTHOR_ID
      join publications as p on ap.PUBLICATION_ID = p.PUBLICATION_ID
      where ahc.HTML_CV_TEXT LIKE concat('%', p.TITLE, '%') and p.JOURNAL <> ''
) `cv_publications` ON (`publications`.`PUBLICATION_ID` = `cv_publications`.`PUBLICATION_ID`)
  LEFT JOIN `utdallas_journals` ON (`journals`.`JOURNAL_ID` = `utdallas_journals`.`JOURNAL_ID`)
  LEFT JOIN `authors_and_departments` ON (`authors+`.`AUTHOR_ID` = `authors_and_departments`.`AUTHOR_ID`)
  LEFT JOIN `departments` ON (`authors_and_departments`.`DEPARTMENT_ID` = `departments`.`DEPARTMENT_ID`)
  LEFT JOIN `google_scholar_author_info` ON (`authors+`.`AUTHOR_ID` = `google_scholar_author_info`.`AUTHOR_ID`)