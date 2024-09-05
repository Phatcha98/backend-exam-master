from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

class TeacherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=10)
    school_id = serializers.IntegerField()

def execute_raw_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        return [dict(zip(columns, row)) for row in results]

class TeacherListView(APIView):
    def get(self, request):
        school_id = request.query_params.get('school')
        classroom_id = request.query_params.get('classroom')
        first_name = request.query_params.get('first_name')
        last_name = request.query_params.get('last_name')
        gender = request.query_params.get('gender')
        
        query = "SELECT * FROM public.teacher"
        params = []
        filters = []
        
        if school_id:
            filters.append("school_id = %s")
            params.append(school_id)
        if classroom_id:
            filters.append("classroom_id = %s")
            params.append(classroom_id)
        if first_name:
            filters.append("first_name LIKE %s")
            params.append(f"%{first_name}%")
        if last_name:
            filters.append("last_name LIKE %s")
            params.append(f"%{last_name}%")
        if gender:
            filters.append("gender = %s")
            params.append(gender)
        
        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        teachers = execute_raw_query(query, params)
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            query = """
                INSERT INTO public.teacher (first_name, last_name, gender, school_id)
                VALUES (%s, %s, %s, %s) RETURNING id
            """
            params = [data['first_name'], data['last_name'], data['gender'], data['school_id']]
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                new_id = cursor.fetchone()[0]
            data['id'] = new_id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherDetailView(APIView):
    def get(self, request, pk):
        query = """
            SELECT t.*, 
            (SELECT array_agg(c.*) FROM public.classroom c WHERE c.teacher_id = t.id) AS classrooms
            FROM public.teacher t WHERE t.id = %s
        """
        teacher = execute_raw_query(query, [pk])
        if not teacher:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TeacherSerializer(teacher[0])
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            query = """
                UPDATE public.teacher SET first_name = %s, last_name = %s, gender = %s, school_id = %s WHERE id = %s
            """
            params = [data['first_name'], data['last_name'], data['gender'], data['school_id'], pk]
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        query = "DELETE FROM public.teacher WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, [pk])
        return Response(status=status.HTTP_204_NO_CONTENT)