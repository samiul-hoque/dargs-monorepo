solution_1_query = """
                SELECT  CONCAT(main.`year`,'_', main.semNo,'_', main.Semester_name) AS yearsem, main.School_name, SUM(main.rv) as Revenue

                FROM
                (SELECT  case dsem.Semester_name WHEN "spring" then 1 WHEN "summer" then 2 WHEN "autumn" then 3 END AS semNo  , ds.School_name, dsem.Semester_name, dsem.`Year` , (dc.Credit_hours*dcls.Enrolled) AS rv
                FROM dargs_school ds 
                INNER JOIN dargs_course dc on ds.School_ID = dc.School_id  
                INNER JOIN dargs_class dcls on dcls.Course_ID_id = dc.Course_ID 
                INNER join dargs_semester dsem on dsem.Semester_ID = dcls.Semester_ID_id 
                ) AS main

                GROUP BY yearsem, main.School_name, main.Semester_name 
                ORDER BY main.School_name, yearsem 
            """

solution_2_query = """
                SELECT ds.School_name, dc.Enrolled, COUNT(dc.Section_No) AS Sections, dsem.Semester_name , dsem.`Year`
                FROM dargs_school ds 
                INNER JOIN dargs_course dcrs ON ds.School_ID =dcrs.School_id 
                INNER JOIN dargs_class dc ON dcrs.Course_ID = dc.Course_ID_id
                INNER JOIN dargs_semester dsem ON dsem.Semester_ID = dc.Semester_ID_id 
                WHERE dc.Enrolled > 0
                GROUP BY dc.Enrolled, ds.School_name 
                ORDER BY ds.School_name, dc.Enrolled, dsem.Semester_name, dsem.`Year`  
            """

solution_3_query = """
                SELECT ds.School_name, AVG(dc.Enrolled) AS "Avg Enroll", AVG(dr.Room_capacity) AS "AVG ROOM", AVG(dr.Room_capacity) - AVG(dc.Enrolled) AS "Difference", (100 -( AVG(dc.Enrolled) /AVG(dr.Room_capacity) ) * 100) AS "Unused %", dsem.Semester_name, dsem.`Year` 
                FROM dargs_class dc 
                INNER JOIN dargs_course dcrs ON dcrs.Course_ID = dc.Course_ID_id 
                INNER JOIN dargs_school ds ON ds.School_ID = dcrs.School_id
                INNER JOIN dargs_room dr ON dc.Room_ID_id = dr.Room_ID
                INNER JOIN dargs_semester dsem ON dsem.Semester_ID = dc.Semester_ID_id 

                GROUP BY ds.School_name, dsem.Semester_name, dsem.`Year`  
            """

solution_4_query = """
                    SELECT 
                        CASE 
                        WHEN main.Class_Size  BETWEEN  1 AND 10 THEN CONCAT("1","-","10") 
                        WHEN main.Class_Size BETWEEN  11 AND 20 THEN CONCAT("11","-","20") 
                        WHEN main.Class_Size BETWEEN  21 AND 30 THEN CONCAT("21","-","30") 
                        WHEN main.Class_Size BETWEEN  31 AND 35 THEN CONCAT("31","-","35") 
                        WHEN main.Class_Size BETWEEN  36 AND 40 THEN CONCAT("36","-","40") 
                        WHEN main.Class_Size BETWEEN  41 AND 50 THEN CONCAT("41","-","50") 
                        WHEN main.Class_Size BETWEEN  51 AND 55 THEN CONCAT("51","-","55") 
                        WHEN main.Class_Size BETWEEN  56 AND 60 THEN CONCAT("56","-","60") 
                        WHEN main.Class_Size > 60 THEN CONCAT("65","-","124") 
                        END AS `Size`, main.department ,main.Sections,main.Semester_name , main.`Year`

                    FROM
                    (
                    SELECT  case SUBSTR(dc.Course_ID_id,1,1) WHEN "C" then "Computer Science" WHEN "E" then "Electrical Engineering" WHEN "P" OR "T" THEN "Physical Sciences" END AS department,dc.Enrolled AS Class_Size, SUM(dc.Section_No) AS Sections, dsem.Semester_name , dsem.`Year`
                    FROM dargs_class dc 
                    INNER JOIN dargs_course dcrs ON dcrs.Course_ID = dc.Course_ID_id  
                    INNER JOIN dargs_school ds ON ds.School_ID = dcrs.School_id 
                    INNER JOIN dargs_semester dsem ON dsem.Semester_ID = dc.Semester_ID_id 
                    WHERE ds.School_name LIKE "SETS" AND dc.Enrolled > 0

                    GROUP BY  department , dsem.`Year`, dsem.Semester_name
                    ORDER BY dc. Enrolled
                    ) AS main
                    GROUP BY `SIZE`, main.`Year`, main.Semester_name
            """

solution_5a_query = """
                SELECT 
                    CASE 
                    WHEN main.Enrolled BETWEEN  1 AND 20 THEN CONCAT("1","-","20") 
                    WHEN main.Enrolled BETWEEN  21 AND 30 THEN CONCAT("21","-","30") 
                    WHEN main.Enrolled BETWEEN  31 AND 35 THEN CONCAT("31","-","35") 
                    WHEN main.Enrolled BETWEEN  36 AND 40 THEN CONCAT("36","-","40") 
                    WHEN main.Enrolled BETWEEN  41 AND 50 THEN CONCAT("41","-","50") 
                    WHEN main.Enrolled BETWEEN  51 AND 54 THEN CONCAT("51","-","54") 
                    WHEN main.Enrolled BETWEEN  55 AND 64 THEN CONCAT("55","-","64") 
                    WHEN main.Enrolled BETWEEN  65 AND 124 THEN CONCAT("65","-","124") 
                    WHEN main.Enrolled BETWEEN  125 AND 168 THEN CONCAT("125","-","168") 
                    END AS Class_Size, COUNT(main.Section_No) as sections, (COUNT(main.Section_No)/14) as "7 Slots",(COUNT(main.Section_No)/16) as "8 Slots", ds.Semester_name , ds.`Year`

                FROM dargs_class main
                INNER JOIN dargs_semester ds ON ds.Semester_ID = main.Semester_ID_id 
                    
                WHERE main.Enrolled <168 AND main.Enrolled > 0
                GROUP BY Class_Size, ds.Semester_name, ds.`Year`
                ORDER BY Class_Size, ds.`Year`,ds.Semester_name
            """

solution_5b_query = """
                SELECT  DISTINCT dr.Room_capacity, COUNT(dr.Room_capacity) as "IUB Resource", SUM(Room_capacity) as "CAPACITY" 
                FROM dargs_room dr 
                GROUP BY dr.Room_capacity 
            """
