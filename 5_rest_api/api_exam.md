
**พัฒนา api ที่ใช้สำหรับเก็บข้อมูลโรงเรียนและบุคลากรในโรงเรียน(นักเรียนและครู) โดยใช้ Django rest framework ต้องมีการใช้งาน serializer และ filter ด้วย django_filter**

## ซึ่งสิ่งที่ต้องพัฒนามีดังนี้

### 1. การเก็บข้อมูล

#### โรงเรียน(school)

- ชื่อโรงเรียน
- ตัวย่อชื่อโรงเรียน
- ที่อยู่

#### ห้องเรียน(classroom)

- ชั้นปี
- ทับ

#### ครู(teacher)

- ชื่อ
- นามสกุล
- เพศ

#### นักเรียน(student)

- ชื่อ
- นามสกุล
- เพศ

**โดยครูจะสามารถอยู่ได้หลายห้องเรียน และแต่ละห้องเรียนก็สามารมีครูได้หลายคน  ในส่วนของนักเรียนสามารถอยู่ได้เพียงห้องเรียนเดียวและในแต่ละห้องเรียนสามารถมีนักเรียนได้หลายคน**

### 2. API

#### school api

- create school
- school list
  can filter with
  - name
- school detail
  in detail want to know
  - count of classroom
  - count of teacher
  - count of student
- update school
- delete school

#### classroom api

- create classroom
- classroom list
  can filter with
  - school
- classroom detail
  in detail want to know
  - list of teacher
  - list of student
- update classroom
- delete classroom

#### teacher api

- create teacher
- teacher list
  can filter with
  - school
  - classroom
  - firstname
  - last name
  - gender
- teacher detail
  in detail want to know
  - list of classroom
- update teacher
- delete teacher

#### student api

- create student
- student list
  can filter with
  - school
  - classroom
  - firstname
  - last name
  - gender
- student detail
  in detail want to know
  - classroom
- update student
- delete student
