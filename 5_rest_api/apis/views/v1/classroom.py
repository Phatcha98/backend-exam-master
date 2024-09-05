from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

class ClassroomSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    school_id = serializers.IntegerField()

def execute_raw_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        return [dict(zip(columns, row)) for row in results]

class ClassroomListView(APIView):
    def get(self, request, *args, **kwargs):
        school_id = request.query_params.get('school')
        query = "SELECT * FROM public.classroom"
        params = []
        if school_id:
            query += " WHERE school_id = %s"
            params.append(school_id)
        classrooms = execute_raw_query(query, params)
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            query = """
                INSERT INTO public.classroom (name, school_id)
                VALUES (%s, %s) RETURNING id
            """
            params = [data['name'], data['school_id']]
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                new_id = cursor.fetchone()[0]
            data['id'] = new_id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassroomDetailView(APIView):
    def get(self, request, pk):
        query = """
            SELECT c.*, 
            (SELECT array_agg(t.*) FROM public.teacher t WHERE t.classroom_id = c.id) AS teachers,
            (SELECT array_agg(s.*) FROM public.student s WHERE s.classroom_id = c.id) AS students
            FROM public.classroom c WHERE c.id = %s
        """
        classroom = execute_raw_query(query, [pk])
        if not classroom:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClassroomSerializer(classroom[0])
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            query = """
                UPDATE public.classroom SET name = %s, school_id = %s WHERE id = %s
            """
            params = [data['name'], data['school_id'], pk]
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        query = "DELETE FROM public.classroom WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, [pk])
        return Response(status=status.HTTP_204_NO_CONTENT)