from django.shortcuts import render
from django.db import connection
import pandas as pd
import numpy as np
from pprint import pprint
from requests import Response
from rest_framework.parsers import FileUploadParser
import io

# Create your views here.
from rest_framework import decorators, request, response, generics, views
from dargs import queries, models
from dargs import serializers
from dargs import utils


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


@decorators.api_view(["GET"])
def analysis_1(request: request.Request):
    semester_years = request.query_params.get(
        "semesters", "2020_spring,2021_autumn,2021_spring"
    ).split(",")
    query_school_name = request.query_params.get("school", "SLASS")

    with connection.cursor() as cursor:
        cursor.execute(queries.solution_1_query)
        data = dictfetchall(cursor)

    transformed = {}

    for instance in data:
        year, _, sem = instance["yearsem"].split("_")
        if f"{year}_{sem}" in semester_years:
            try:
                transformed[instance["yearsem"]].append(
                    {
                        "School_name": instance["School_name"],
                        "Revenue": instance["Revenue"],
                    }
                )
            except:
                transformed[instance["yearsem"]] = [
                    {
                        "School_name": instance["School_name"],
                        "Revenue": instance["Revenue"],
                    }
                ]

    revenue_info = {}

    for key in transformed:
        rev = 0
        revenue_info[key] = rev
        school_info = transformed[key]
        for school in school_info:
            rev += school["Revenue"]
        revenue_info[key] = rev

    revenue_chart_data = {"columns": list(transformed.keys()), "values": []}
    all_schools = set()

    for semester in transformed.keys():
        rev_schools = transformed[semester]
        for rev_instance in rev_schools:
            all_schools.add(rev_instance["School_name"])
            if rev_instance["School_name"] == query_school_name:
                revenue_chart_data["values"].append(int(rev_instance["Revenue"]))

    pprint(revenue_chart_data)

    return response.Response(
        data={
            "revenueTable": transformed,
            "revenueSummary": revenue_info,
            "revenueChart": revenue_chart_data,
            "tableColumns": ["Semester"] + list(all_schools) + ["Total"],
        },
        status=200,
    )


@decorators.api_view(["GET"])
def analysis_2(request: request.Request):
    try:
        year_semester = request.query_params.get("year_semester", "2021_autumn")
        year, semester = year_semester.split("_")
        enrolled = request.query_params.get("max_enrolled", 20)
        enrolled = int(enrolled)

        with connection.cursor() as cursor:
            cursor.execute(queries.solution_2_query)
            data = dictfetchall(cursor)

        df = pd.DataFrame(data)

        df = df[(df.Year == int(year)) & (df.Semester_name == semester)]
        del df["Year"]
        del df["Semester_name"]
        df = df.pivot_table(
            index="Enrolled", columns=["School_name"], aggfunc=np.sum, fill_value=0
        )
        df.columns = [c[1] for c in df.columns.values]
        df.reset_index(inplace=True)

        def conditional_sum(data_dict):
            total = 0
            for k, v in data_dict.items():
                if k != "Enrolled":
                    total += v
            return total

        df["Total"] = df.apply(conditional_sum, axis=1)
        df = df[df.Enrolled <= enrolled]

        return response.Response(
            data={
                "tabularData": df.to_dict("records"),
                "columns": list(df.columns),
                "semester": year_semester,
            }
        )

    except Exception as e:
        return response.Response(
            data={"tabularData": [], "columns": [], "semester": year_semester}
        )


@decorators.api_view(["GET"])
def analysis_3(request: request.Request):
    semester_year = request.query_params.get("semester", "2020_spring")
    with connection.cursor() as cursor:
        cursor.execute(queries.solution_3_query)
        data = dictfetchall(cursor)
    df = pd.DataFrame(data)
    df["semester_year"] = df.apply(
        lambda x: f"{x['Year']}_{x['Semester_name']}", axis=1
    )
    df = df[df.semester_year == semester_year]
    del df["semester_year"]
    return response.Response(
        data={
            "tabularData": df.to_dict("records"),
            "columns": list(df.columns),
            "semester": semester_year,
        }
    )


@decorators.api_view(["GET"])
def analysis_4(request: request.Request):
    semester_year = request.query_params.get("semester", "2020_spring")
    _ranges = request.query_params.get("ranges", "1-10").split(",")

    with connection.cursor() as cursor:
        cursor.execute(queries.solution_4_query)
        data = dictfetchall(cursor)

    df = pd.DataFrame(data)
    df["semester_year"] = df.apply(
        lambda x: f"{x['Year']}_{x['Semester_name']}", axis=1
    )
    df = df[(df.semester_year == semester_year) & (df.Size.isin(_ranges))]
    del df["semester_year"]

    return response.Response(
        data={
            "tabularData": df.to_dict("records"),
            "columns": list(df.columns),
            "semester": semester_year,
        }
    )


@decorators.api_view(["GET"])
def analysis_5(request: request.Request):
    year_semester = request.query_params.get("semester", "2020_autumn")
    year, semester = year_semester.split("_")
    year = int(year)
    _ranges = request.query_params.get("ranges", "1-10").split(",")

    with connection.cursor() as cursor:
        cursor.execute(queries.solution_5a_query)
        data_a = dictfetchall(cursor)

    df_a = pd.DataFrame(data_a)
    df_a = df_a[
        (df_a.Year == year)
        & (df_a.Semester_name == semester)
        & (df_a.Class_Size.isin(_ranges))
    ]
    del df_a["Year"]
    del df_a["Semester_name"]
    df_a = pd.concat(
        [
            df_a,
            pd.Series(
                {
                    "Class_Size": "Total",
                    "sections": df_a.sections.sum(),
                    "7 Slots": df_a["7 Slots"].sum(),
                    "8 Slots": df_a["8 Slots"].sum(),
                }
            )
            .to_frame()
            .T,
        ]
    )

    return response.Response(
        data={
            "tabularData": df_a.to_dict("records"),
            "columns": list(df_a.columns),
            "semester": year_semester,
        }
    )


@decorators.api_view(["GET"])
def analysis_6(request: request.Request):

    with connection.cursor() as cursor:
        cursor.execute(queries.solution_5b_query)
        data_b = dictfetchall(cursor)

    df_b = pd.DataFrame(data_b)

    return response.Response(
        data={
            "tabularData": df_b.to_dict("records"),
            "columns": list(df_b.columns),
        }
    )


class SemesterListView(generics.ListAPIView):
    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer


class SchoolListView(generics.ListAPIView):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer


@decorators.api_view(["GET"])
def analysis_range_sizes(request):
    analysis_no = request.query_params.get("analysis", 4)
    analysis_no = int(analysis_no)
    if analysis_no == 4:
        return response.Response(
            data={
                "ranges": [
                    "1-10",
                    "11-20",
                    "21-30",
                    "31-35",
                    "36-40",
                    "41-50",
                    "51-55",
                    "56-60",
                    "60+",
                ]
            }
        )
    elif analysis_no == 5:
        return response.Response(
            data={
                "ranges": [
                    "1-20",
                    "21-30",
                    "31-35",
                    "36-40",
                    "41-50",
                    "51-54",
                    "55-64",
                    "65-124",
                    "125-168",
                ]
            }
        )


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, filename, format=None):
        file_obj = request.data["file"]
        file_obj.seek(0)
        file_name = file_obj.name
        file_extension = file_name.split(".")[-1]
        print(file_name, file_extension)

        if file_extension != "csv":
            return response.Response(
                data={"error": "File extension not supported"}, status=400
            )

        stringio = io.StringIO(file_obj.read().decode("utf-8"))
        stringio.seek(0)

        df = pd.read_csv(stringio, skiprows=7)[:-3]
        df = utils.preprocess(df, file_name)
        utils.insert_to_db(df)

        return response.Response(data={"success": True})


@decorators.api_view(["DELETE"])
def clear_db(request):
    utils.reset_db()
    utils.call_command("makemigrations", "dargs")
    utils.call_command("migrate", "dargs")
    utils.call_command("migrate")

    return response.Response(data={"cleared": True})
