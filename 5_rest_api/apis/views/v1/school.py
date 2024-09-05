from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class SchoolSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    short_name = serializers.CharField(max_length=20)
    address = serializers.CharField()

def execute_raw_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        return [dict(zip(columns, row)) for row in results]

class SchoolListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        name = request.query_params.get('name')
        query = "SELECT * FROM public.school"
        params = []
        if name:
            query += " WHERE name LIKE %s"
            params.append(f"%{name}%")
        schools = execute_raw_query(query, params)
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            query = """
                INSERT INTO public.school (name, short_name, address)
                VALUES (%s, %s, %s) RETURNING id
            """
            params = [data['name'], data['short_name'], data['address']]
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                new_id = cursor.fetchone()[0]
            data['id'] = new_id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SchoolDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        query = """
            SELECT s.*, 
            (SELECT COUNT(*) FROM public.classroom WHERE school_id = s.id) AS classroom_count,
            (SELECT COUNT(*) FROM public.teacher WHERE school_id = s.id) AS teacher_count,
            (SELECT COUNT(*) FROM public.student WHERE school_id = s.id) AS student_count
            FROM public.school s WHERE s.id = %s
        """
        school = execute_raw_query(query, [pk])
        if not school:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SchoolSerializer(school[0])
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            query = """
                UPDATE public.school SET name = %s, short_name = %s, address = %s WHERE id = %s
            """
            params = [data['name'], data['short_name'], data['address'], pk]
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        query = "DELETE FROM public.school WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, [pk])
        return Response(status=status.HTTP_204_NO_CONTENT)