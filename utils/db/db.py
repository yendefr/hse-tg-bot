from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from loader import db

class DB():
    pool: Connection = db

    CHECK_STUDENT = "SElECT COUNT(*) FROM students WHERE name = $1"
    CHECK_TEACHER = "SElECT COUNT(*) FROM teachers WHERE name = $1"
    CHECK_TEACHER_BY_ID = "SElECT COUNT(*) FROM teachers WHERE id = $1"
    CHECK_PASSWORD_S = "SELECT password FROM students WHERE name = $1"
    CHECK_PASSWORD_T = "SELECT password FROM teachers WHERE name = $1"
    UPDATE_STUDENT_ID = "UPDATE students SET id = $1 WHERE name = $2"
    UPDATE_TEACHER_ID = "UPDATE teachers SET id = $1 WHERE name = $2"
    UPDATE_STUDENT_EMAIL = "UPDATE students SET email = $1 WHERE name = $2"
    UPDATE_TEACHER_EMAIL = "UPDATE teachers SET email = $1 WHERE name = $2"
    UPDATE_SCHEDULE_ID = "UPDATE schedule SET teacher_id = $1 WHERE teacher_id = $2"

    INSERT_STUDENT = "INSERT INTO students(name, email, password, group_id) VALUES ($1, $2, $3, $4)"
    INSERT_TEACHER = "INSERT INTO teachers(name, email, password) VALUES ($1, $2, $3)"
    INSERT_SCHEDULE = "INSERT INTO schedule(teacher_id, class, time, subject, group_id) VALUES ($1, $2, $3, $4, $5)"
    UPDATE_IS_SICK = "UPDATE students SET is_sick = $1 WHERE id = $2"

    GET_SCHEDULE = "SELECT * FROM schedule WHERE teacher_id = $1"
    GET_TEACHER_ID_BY_NAME = "SELECT id FROM teachers WHERE name = $1"
    GET_SICKED = "SELECT name FROM students WHERE is_sick = true AND group_id = $1"

    async def check_student(self, name):
        return await self.pool.fetchval(self.CHECK_STUDENT, name)

    async def check_teacher(self, name):
        return await self.pool.fetchval(self.CHECK_TEACHER, name)
    
    async def check_teacher_by_id(self, id):
        return await self.pool.fetchval(self.CHECK_TEACHER_BY_ID, id)
    
    async def check_password_s(self, name):
        return await self.pool.fetchval(self.CHECK_PASSWORD_S, name)
    
    async def check_password_t(self, name):
        return await self.pool.fetchval(self.CHECK_PASSWORD_T, name)

    async def update_student_id(self, user_id, name):
        return await self.pool.fetchval(self.UPDATE_STUDENT_ID, user_id, name)
    
    async def update_teacher_id(self, user_id, name):
        return await self.pool.fetchval(self.UPDATE_TEACHER_ID, user_id, name)
    
    async def update_student_email(self, email, name):
        return await self.pool.fetchval(self.UPDATE_STUDENT_EMAIL, email, name)
    
    async def update_teacher_email(self, email, name):
        return await self.pool.fetchval(self.UPDATE_TEACHER_EMAIL, email, name)
    
    async def update_is_sick(self, user_id, is_sick):
        return await self.pool.fetchval(self.UPDATE_IS_SICK, is_sick, user_id)

    async def update_schedule_id(self, new_id, old_id):
        return await self.pool.fetchval(self.UPDATE_SCHEDULE_ID, new_id, old_id)

    async def get_teacher_id_by_name(self, name):
        return await self.pool.fetchval(self.GET_TEACHER_ID_BY_NAME, name)
    
    async def get_schedule(self, teacher_id):
        return await self.pool.fetch(self.GET_SCHEDULE, teacher_id)
    
    async def get_sicked(self, group_id):
        return await self.pool.fetch(self.GET_SICKED, group_id)

    async def insert(self, table, args):
        if (table == 'students'): command = self.INSERT_STUDENT
        if (table == 'teachers'): command = self.INSERT_TEACHER
        if (table == 'schedule'): command = self.INSERT_SCHEDULE
        print('Команда:', command, *args)
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass
