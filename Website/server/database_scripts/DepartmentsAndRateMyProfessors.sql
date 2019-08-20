SET SESSION group_concat_max_len = 1000000;
Select d.DEPARTMENT_ID, d.DEPARTMENT_NAME, a.FIRST_NAME, rp.TFNAME, a.LAST_NAME, rp.OVERALL_RATING, concat('[',group_concat(concat('{"comment":"',replace(replace(rs.RCOMMENTS,'"','\\\"'), "\r"," "),'"}')),']') as ratingComments from departments as d
	join authors_and_departments as ad on d.DEPARTMENT_ID = ad.DEPARTMENT_ID
    join authors as a on a.AUTHOR_ID = ad.AUTHOR_ID
    left join rate_my_professors_professors as rp on (left(rp.TFNAME, 1) = left(a.FIRST_NAME, 1) or rp.TFNAME = a.MIDDLE_NAME) and rp.TLNAME = a.LAST_NAME
    left join rate_my_professors_student_ratings as rs on rs.RATE_MY_PROFESSORS_PROFESSOR_ID = rp.RATE_MY_PROFESSORS_PROFESSOR_ID 
    group by a.AUTHOR_ID
    order by d.DEPARTMENT_ID, a.AUTHOR_ID