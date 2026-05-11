from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, CustomMoviePagination
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter()


@router.get("/movies", response_model=CustomMoviePagination)
async def read_movies(
        page: int = Query(1, ge=1, description="The page number to fetch."),
        per_page: int = Query(10, ge=1, le=20, description="Number of movies per page."),
        db: AsyncSession = Depends(get_db)):
    total_count = await db.scalar(select(func.count()).select_from(MovieModel))
    if total_count == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    from fastapi_pagination import Params
    params = Params(page=page, size=per_page)

    return await paginate(db, select(MovieModel), params=params)


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    movie = await db.scalar(query)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
