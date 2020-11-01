import pytest

TODOS_MAX = 200
TODOS_HALF = TODOS_MAX // 2


# Positive/negative tests for Getting a resource.
@pytest.mark.parametrize('todo_id', [1, 2, TODOS_HALF, TODOS_MAX - 1, TODOS_MAX])
def test_get_positive(session, base_url, todo_id):
    res = session.get(url=f'{base_url}/{todo_id}')

    assert res.status_code == 200
    assert res.json()['id'] == todo_id


@pytest.mark.parametrize('todo_id', [-1, 0, TODOS_MAX + 1, TODOS_MAX ** 100, 2.5, 'test', '@', 'тест'])
def test_get_negative(session, base_url, todo_id):
    res = session.get(url=f'{base_url}/{todo_id}')

    assert res.status_code == 404
    assert res.json() == {}


# Positive tests for Listing all resources.
def test_get_all_positive(session, base_url):
    res = session.get(url=f'{base_url}')

    assert res.status_code == 200
    assert res.json()
    assert len(res.json()) == TODOS_MAX


# Positive tests for Creating a resource.
def test_post_positive(session, base_url):
    title = "Todo title"
    completed = False
    payload = {'title': title, 'completed': completed, 'userId': 1}
    res = session.post(url=base_url, json=payload)

    assert res.status_code == 201
    res_json = res.json()
    assert res_json['id'] == TODOS_MAX + 1
    assert res_json['userId'] == 1
    assert res_json['title'] == title
    assert res_json['completed'] == completed


# Positive/negative tests for Updating a resource with PUT.
@pytest.mark.parametrize('user_id, todo_id',
                         [(1, 1),
                          (1, 11),
                          (1, 20),
                          (2, 21),
                          (7, 140),
                          (10, 200)])
def test_put_positive(session, base_url, user_id, todo_id):
    title = f'New title for user_id={user_id} and todo_id={todo_id}'
    completed = True
    payload = {'title': title, 'completed': completed, 'userId': user_id, 'id': todo_id}
    res = session.put(url=f'{base_url}/{todo_id}', json=payload)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['title'] == title
    assert res_json['completed'] == completed
    assert res_json['userId'] == user_id
    assert res_json['id'] == todo_id


@pytest.mark.parametrize('user_id, todo_id',
                         [(0, 1),
                          (-1, 1),
                          (-9999999999999, 1),
                          (2.5, 1),
                          ('test', 1),
                          (' ', 1),
                          ('-', 1),
                          (11, 1)])
def test_put_user_id_negative(session, base_url, user_id, todo_id):
    title = f'New title for user_id={user_id} and todo_id={todo_id}'
    completed = True
    payload = {'title': title, 'completed': completed, 'userId': user_id, 'id': todo_id}
    res = session.put(url=f'{base_url}/{todo_id}', json=payload)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['title'] == title
    assert res_json['completed'] == completed
    assert res_json['userId'] == user_id
    assert res_json['id'] == todo_id


@pytest.mark.parametrize('user_id, todo_id',
                         [(3, -1),
                          (3, 0),
                          (3, 2.5),
                          (3, TODOS_MAX + 1),
                          (3, 'test'),
                          (3, ' '),
                          (3, '-'),
                          (3, 10000000000000),
                          (3, '%D0%B0%D0%BF%D0%B8')])
def test_put_todo_id_negative(session, base_url, user_id, todo_id):
    title = f'New title for user_id={user_id} and todo_id={todo_id}'
    completed = True
    payload = {'title': title, 'completed': completed, 'userId': user_id, 'id': todo_id}
    res = session.put(url=f'{base_url}/{todo_id}', json=payload)

    assert res.status_code == 500


# Positive tests for Updating a resource with PATCH
@pytest.mark.parametrize('todo_id, title',
                         [(1, 'New title for todo_id=1'),
                          (2, 'New title for todo_id=2'),
                          (10, 'New title for todo_id=10'),
                          (11, 'New title for todo_id=11'),
                          (200, 'New title for todo_id=200')])
def test_patch_title_positive(session, base_url, todo_id, title):
    payload = {'title': title}
    res = session.patch(url=f'{base_url}/{todo_id}', json=payload)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['title'] == title
    assert res_json['id'] == todo_id


@pytest.mark.parametrize('todo_id, completed',
                         [(1, True),
                          (2, True),
                          (10, False),
                          (11, False),
                          (200, True)])
def test_patch_completed_positive(session, base_url, todo_id, completed):
    payload = {'completed': completed}
    res = session.patch(url=f'{base_url}/{todo_id}', json=payload)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['completed'] == completed
    assert res_json['id'] == todo_id


# Positive tests for Deleting a resource
@pytest.mark.parametrize('todo_id', [1, 2, TODOS_HALF, TODOS_MAX - 1, TODOS_MAX])
def test_delete_positive(session, base_url, todo_id):
    res = session.get(url=f'{base_url}/{todo_id}')

    assert res.status_code == 200
    assert res.json()['id'] == todo_id


# Positive/negative tests for Filtering resources.
@pytest.mark.parametrize('user_id', [1, 2, 5, 9, 10])
def test_filtering_by_user_id_positive(session, base_url, user_id):
    res = session.get(url=f'{base_url}?userId={user_id}')

    assert res.status_code == 200
    for item in res.json():
        assert item['userId'] == user_id


@pytest.mark.parametrize('todo_id', [1, 2, 100, 199, 200])
def test_filtering_by_todo_id_positive(session, base_url, todo_id):
    res = session.get(url=f'{base_url}?id={todo_id}')

    assert res.status_code == 200
    for item in res.json():
        assert item['id'] == todo_id


@pytest.mark.parametrize('title', ['ut cupiditate sequi aliquam fuga maiores',
                                   'inventore saepe cumque et aut illum enim',
                                   'excepturi a et neque qui expedita vel voluptate',
                                   'numquam repellendus a magnam',
                                   'ipsam aperiam voluptates qui'])
def test_filtering_by_todo_id_positive(session, base_url, title):
    res = session.get(url=f'{base_url}?id={title}')

    assert res.status_code == 200
    for item in res.json():
        assert item['title'] == title


@pytest.mark.parametrize('completed', [True, False])
def test_filtering_by_completed_positive(session, base_url, completed):
    res = session.get(url=f'{base_url}?completed={completed}')

    assert res.status_code == 200
    for item in res.json():
        assert item['completed'] == completed


@pytest.mark.parametrize('user_id', [0, -1, -9999999999999, 2.5, 'test', ' ', '-'])
def test_filtering_by_user_id_negative(session, base_url, user_id):
    res = session.get(url=f'{base_url}?userId={user_id}')

    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.parametrize('todo_id', [0, -1, -9999999999999, 2.5, TODOS_MAX + 1, 'test', ' ', '-'])
def test_filtering_by_todo_id_negative(session, base_url, todo_id):
    res = session.get(url=f'{base_url}?id={todo_id}')

    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.parametrize('title', [0, -1, 2.5, 'wrong title', ' ', '-'])
def test_filtering_by_title_negative(session, base_url, title):
    res = session.get(url=f'{base_url}?title={title}')

    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.parametrize('completed', [0, -1, -9999999999999, 2.5, 'test', ' ', '-'])
def test_filtering_by_completed_negative(session, base_url, completed):
    res = session.get(url=f'{base_url}?completed={completed}')

    assert res.status_code == 200
    assert res.json() == []
