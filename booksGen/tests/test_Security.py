from jwt import decode

from booksgen.security import create_access_token, Settings


def test_create_jwt():
    data = {'sub': 'test@test.com'}

    token_generate=create_access_token(data)

    result=decode(
        token_generate, 
        key=Settings().SECRET_KEY, 
        algorithms=[Settings().ALGORITHM]
    )
    
    assert result['sub'] == data['sub']
    assert result['exp']
