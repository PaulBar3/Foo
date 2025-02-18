from fastapi import HTTPException
from database import new_session
from models import ExpenseModel
from schemas import ExpenseAddSchema, ExpenseSchema, ExpenseUpdateSchema
from sqlalchemy import delete, select


class ExpenseRepository:
    @classmethod
    async def add_expenses(cls, data: ExpenseAddSchema) -> int:
        async with new_session() as session:
            expense_dict = data.model_dump()

            expense = ExpenseModel(**expense_dict)
            session.add(expense)
            await session.flush()
            await session.commit()
            return expense.id

    @classmethod
    async def get_expenses(cls) -> list[ExpenseSchema]:
        async with new_session() as session:
            query = select(ExpenseModel)
            result = await session.execute(query)
            expense_models = result.scalars().all()
            #expense_models_id = [expense.id for expense in expense_models]
            return expense_models
        

    @classmethod
    async def get_expenses_by_id(cls, expense_id: int) -> ExpenseSchema:
        async with new_session() as session:
            query = select(ExpenseModel).where(ExpenseModel.id == expense_id)
            result = await session.execute(query)
            expense = result.scalars().first()

            if not expense:
                raise HTTPException(status_code=404, detail="Expense not found")

            return expense



    @classmethod
    async def update_expense(cls, expense_id: int, data: ExpenseUpdateSchema) -> ExpenseSchema:
        async with new_session() as session:
            # Получаем текущую запись
            query = select(ExpenseModel).where(ExpenseModel.id == expense_id)
            result = await session.execute(query)
            expense = result.scalars().first()

            if not expense:
                raise HTTPException(status_code=404, detail="Expense not found")

            
            expense_dict = data.model_dump(exclude_unset=True) 
            for key, value in expense_dict.items():
                setattr(expense, key, value)

            await session.commit()
            await session.refresh(expense)
            return expense
        

    @classmethod
    async def delete_expense(cls, expense_id: int) -> bool:
        async with new_session() as session:
            query = select(ExpenseModel).where(ExpenseModel.id == expense_id)
            result = await session.execute(query)
            expense = result.scalars().first()

            if not expense:
                raise HTTPException(status_code=404, detail="Expense not found")

            
            delete_query = delete(ExpenseModel).where(ExpenseModel.id == expense_id)
            await session.execute(delete_query)
            await session.commit()
            return True   