from typing import Annotated
from fastapi import APIRouter, Depends
from repository import ExpenseRepository
from schemas import ExpenseSchema, ExpenseAddSchema, ExpenseUpdateSchema


router = APIRouter(prefix="/expenses", tags=["Расходы"])


@router.get("/",response_model=list[ExpenseSchema])
async def get_expenses() -> list[ExpenseSchema]:
    expense = await ExpenseRepository.get_expenses()
    return expense
            
            


@router.get("/{expense_id}")
async def get_expense_by_id(expense_id: int) -> ExpenseSchema:
    expense = await ExpenseRepository.get_expenses_by_id(expense_id)
    return expense



@router.post("/")
async def add_expense(
    expense:Annotated[ExpenseSchema, Depends(ExpenseAddSchema)]) -> dict:
    expense_id = await ExpenseRepository.add_expenses(expense)
    return {'id': expense_id, "ok": 'Запись успешно добавлена', 'expense': expense, }


@router.put("/{expense_id}")
async def update_expense(
    expense_id: int,
    expense: Annotated[ExpenseUpdateSchema, Depends(ExpenseSchema)]) -> ExpenseSchema:
    expense = await ExpenseRepository.update_expense(expense_id, expense)


@router.delete("/{expense_id}")
async def delete_expense(expense_id: int) -> bool:
    return await ExpenseRepository.delete_expense(expense_id)