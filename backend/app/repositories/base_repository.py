from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from typing import TypeVar, Any, Generic, Optional, Dict, List, Tuple


ModelType = TypeVar("ModelType", bound=Any)


class BaseRepository(Generic[ModelType]):

    """
    Base repository class to be inherited by other repositories.
    """

    def __init__(self, db: AsyncSession, model: ModelType):
        """
        Initialize the repository with the database session and model.
        Args:
            db: SQLAlchemy AsyncSession object.
            model: SQLAlchemy model class.
        """
        self.db = db
        self.model = model


    async def exists(self, **kwargs) -> bool:
        """
        Check if a record exists based on provided filters.
        Example: exists(email="a@b.com")

        Args:
            **kwargs: Filter conditions as keyword arguments.
        """
        query = select(self.model).filter_by(**kwargs)
        result = await self.db.execute(query)
        return result.scalars().one_or_none() is not None


    async def get(self, *, id: UUID) -> Optional[ModelType]:
        """
        Get a record by its ID.

        Args:
            id: UUID of the record to retrieve.
        
        Returns:
            The record if found, else None.
        """
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()


    async def get_by_id(self, id: UUID) -> Optional[ModelType]:
        
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()


    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by = None
    ) -> Tuple[List[ModelType], int]:
        """
        Generic list method with optional filters + simple pagination.
        Returns (items, total_count).
        """
        filters = filters or {}
        query = select(self.model)
        count_q = select(func.count()).select_from(self.model)

        # apply exact-match filters (extend later as needed)
        for key, value in filters.items():
            column = getattr(self.model, key, None)
            if column is not None:
                query = query.where(column == value)
                count_q = count_q.where(column == value)

        if order_by is not None:
            query = query.order_by(order_by)

        query = query.offset(offset).limit(limit)
        result = await self.db.execute(query)
        items = result.scalars().all()

        total_res = await self.db.execute(count_q)
        total = total_res.scalar_one()
        return items, total


    async def create(
        self, 
        *, 
        obj_in: Dict[str, Any], 
        commit_transaction: Optional[bool] = True
    ) -> ModelType:
        """
        Create a new record in the database.

        Args:
            obj_in: Dictionary containing the data for the new record.
            commit_transaction: Whether to commit the transaction after adding the record.
        
        Returns:
            The newly created record.
        """

        # handle enum values by converting to their string representation
        processed_data = {}
        for key, value in obj_in.items():
            if hasattr(value, 'value'):
                processed_data[key] = value.value
            else:
                processed_data[key] = value

        # Create the database object
        db_obj = self.model(**processed_data)
        self.db.add(db_obj)
        if commit_transaction:
            await self.db.commit()
            await self.db.refresh(db_obj)
        return db_obj


    async def update(
        self,
        *,
        db_model: ModelType,
        obj_in: Dict[str, Any],
        commit_transaction: Optional[bool] = True
    ) -> Optional[ModelType]:
        
        """
        Update an existing record in the database.

        Args:
            id: UUID of the record to update.
            obj_in: Dictionary containing the updated data.
            commit_transaction: Whether to commit the transaction after updating the record.

        Returns:
            The updated record if found, else None.
        """

        # # Check if record exists
        # db_obj = await self.get_by_id(id)
        # if not db_obj:
        #     return None
        
        # Update the record's attributes
        for key, value in obj_in.items():
            setattr(db_model, key, value)

        if commit_transaction:
            self.db.add(db_model)
            await self.db.commit()
            await self.db.refresh(db_model)
        
        return db_model


    async def delete(
        self,
        *,
        db_model: ModelType,
        commit_transaction: Optional[bool] = True
    ) -> Optional[ModelType]:
        """
        Delete a record by its ID.

        Args:
            id: UUID of the record to delete.

        Returns:
            The deleted record if found, else None.
        """

        # Check uf record exists
        # db_obj = await self.read(id)
        # if not db_obj:
        #     return None

        await self.db.delete(db_model)

        if commit_transaction:
            await self.db.commit()
