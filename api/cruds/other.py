from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import Optional, Tuple

import api.models as fff_model
import api.schemas as fff_schema

# d888888b d8888b.  .d8b.  d8b   db .d8888.  .d8b.   .o88b. d888888b d888888b  .d88b.  d8b   db 
# `~~88~~' 88  `8D d8' `8b 888o  88 88'  YP d8' `8b d8P  Y8 `~~88~~'   `88'   .8P  Y8. 888o  88 
#    88    88oobY' 88ooo88 88V8o 88 `8bo.   88ooo88 8P         88       88    88    88 88V8o 88 
#    88    88`8b   88~~~88 88 V8o88   `Y8b. 88~~~88 8b         88       88    88    88 88 V8o88 
#    88    88 `88. 88   88 88  V888 db   8D 88   88 Y8b  d8    88      .88.   `8b  d8' 88  V888 
#    YP    88   YD YP   YP VP   V8P `8888Y' YP   YP  `Y88P'    YP    Y888888P  `Y88P'  VP   V8P 
                                                                                              
# d888888b db    db d8888b. d88888b .d8888.                                                     
# `~~88~~' `8b  d8' 88  `8D 88'     88'  YP                                                     
#    88     `8bd8'  88oodD' 88ooooo `8bo.                                                       
#    88       88    88~~~   88~~~~~   `Y8b.                                                     
#    88       88    88      88.     db   8D                                                     
#    YP       YP    88      Y88888P `8888Y'                                                     
                                                                                              
                                                                                              
async def get_transaction_type(id: int, db: AsyncSession) -> Optional[fff_model.TransactionType]:
	result: Result = await db.execute(
		select(fff_model.TransactionType).filter(fff_model.TransactionType.id == id)
	)
	t: Optional[Tuple[fff_model.TransactionType]] = result.fetchone()
	return t[0] if t is not None else None

async def get_transaction_types(category: fff_schema.TransactionTypeCategory, db: AsyncSession) -> list[fff_model.TransactionType]:
	result: Result = await db.execute(
		select(fff_model.TransactionType).filter(fff_model.TransactionType.category == category)
	)
	tt_list = list(map(lambda x: x[0], result.fetchall()))
	return tt_list


# .d8888. d88888b  .d8b.  d8888b.  .o88b. db   db 
# 88'  YP 88'     d8' `8b 88  `8D d8P  Y8 88   88 
# `8bo.   88ooooo 88ooo88 88oobY' 8P      88ooo88 
#   `Y8b. 88~~~~~ 88~~~88 88`8b   8b      88~~~88 
# db   8D 88.     88   88 88 `88. Y8b  d8 88   88 
# `8888Y' Y88888P YP   YP 88   YD  `Y88P' YP   YP 

async def search_transactions(query: str, db: AsyncSession) -> list[fff_model.Transaction]:
	result: Result = await db.execute(
		select(fff_model.Transaction).filter(fff_model.Transaction.description.like(query))
	)
	t_list = list(map(lambda x: x[0], result.fetchall()))
	return t_list

# .d8888. db    db .88b  d88. .88b  d88.  .d8b.  d8888b. db    db 
# 88'  YP 88    88 88'YbdP`88 88'YbdP`88 d8' `8b 88  `8D `8b  d8' 
# `8bo.   88    88 88  88  88 88  88  88 88ooo88 88oobY'  `8bd8'  
#   `Y8b. 88    88 88  88  88 88  88  88 88~~~88 88`8b      88    
# db   8D 88b  d88 88  88  88 88  88  88 88   88 88 `88.    88    
# `8888Y' ~Y8888P' YP  YP  YP YP  YP  YP YP   YP 88   YD    YP    


# d8888b.  .d8b.  db       .d8b.  d8b   db  .o88b. d88888b 
# 88  `8D d8' `8b 88      d8' `8b 888o  88 d8P  Y8 88'     
# 88oooY' 88ooo88 88      88ooo88 88V8o 88 8P      88ooooo 
# 88~~~b. 88~~~88 88      88~~~88 88 V8o88 8b      88~~~~~ 
# 88   8D 88   88 88booo. 88   88 88  V888 Y8b  d8 88.     
# Y8888P' YP   YP Y88888P YP   YP VP   V8P  `Y88P' Y88888P 
                                                         
                                                         