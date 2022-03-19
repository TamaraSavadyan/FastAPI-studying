from typing import List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2  # '..' means going to upper directory
# if current directory is even more lower then our modules, add another dot -> '...'
from ..database import get_db

router = APIRouter (
    prefix="/posts",
    tags=['Posts']
)


# to get list of posts need to import class "List" from module "typing"
@router.get("/", response_model=List[schemas.PostResponse])
def getPosts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    cursor.execute("""SELECT * FROM posts""") # need a cursor to interact with database
    posts = cursor.fetchall() # in order to get the result need to use function "fetch(all/one)"
    '''
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createPosts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    '''
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                                                (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()  # need to commit changes to database
    '''
    print(current_user.email)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())  # this ** method unpacks dictionary,
    # so we don't have to type every name/value manually
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # this function stands for "RETURNING * " sql command
    # it retrieves post data back to variable 'new_post'
    # (what's the point? I already got this variable with all contents)

    return new_post


# Order actually MATTERS.
# If I would put "getLatestPost" function after "getPost" func,
# programm would give me an error,
# because it would take my word "latest" as the argument for function "getPost"
'''
@router.get("/posts/latest")
def getLatestPost():
    post = myPosts[len(myPosts) - 1]
    return {"detail": post}
'''


# {id} field is called "path parameter"
@router.get("/{id}", response_model=schemas.PostResponse)
# def getPost(id: int, response: Response):  # variable validation (if it has to be specific type)
# when we raising exception inside function we don't need to store response manually
def getPost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    post = cursor.fetchone()
    '''
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    deleted_post = cursor.fetchone()
    conn.commit()
    '''
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} doesn't exist")

    # smth from sqlalchemy documentation (in order to everything work correctly)
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def updatePost(id: int, post:  schemas.PostCreate, db: Session = Depends(get_db), 
               current_user: int = Depends(oauth2.get_current_user)):
    '''
    cursor.execute("""UPDATE posts 
                    SET title = %s, content = %s, published = %s
                    WHERE id = %s
                    RETURNING * """,
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    '''
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} doesn't exist")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_post.first()
