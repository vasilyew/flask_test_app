from aiohttp import ClientSession
import asyncio


n = 3


async def get(url):
    try:
        async with ClientSession() as session:
            async with session.get(url, timeout=2) as response:
                if response.status != 200:
                    return []
                res = await response.json()
    except Exception:
        return []
    return res



async def get_source_data(url):
    try:
        return await asyncio.wait_for(get(url), timeout=2.0)
    except asyncio.TimeoutError:
        return []


async def get_users_data():
    url_template = 'http://127.0.0.1:5000/static/source%d.json'
    tasks = []
    for i in range(n):
        url = url_template % (i + 1)
        task = asyncio.ensure_future(get_source_data(url))
        tasks.append(task)
    responses = await asyncio.gather(*tasks)
    data = user_data_mapper(responses)
    return data


def user_data_mapper(responses):
    middle_list = []
    for i in range(n):
        middle_list.append(search_middle((i + 1) * 10, responses[i]))
    result = []
    for i in range(n):
        if middle_list[i] is None or middle_list[i] == 'r':
            continue
        elif middle_list[i] == 'l':
            result.extend(responses[i])
        else:
            result.extend(responses[i][0:middle_list[i]+1])
    for i in range(n):
        if middle_list[i] is None or middle_list[i] == 'l':
            continue
        elif middle_list[i] == 'r':
            result.extend(responses[i])
        else:
            result.extend(responses[i][middle_list[i]+1:])
    return result


def search_middle(middle_index, user_collect):
    l = len(user_collect)
    if l == 0:
        return None
    if l == 1 and user_collect[0]['id'] <= middle_index:
        return 'l'
    if l == 1 and user_collect[0]['id'] > middle_index:
        return 'r'
    
    return search_middle_binnary(middle_index, 0, l - 1, user_collect, l)


def search_middle_binnary(middle_index, start_item, end_item, user_collect, length):
    middle_item = start_item + (end_item - start_item) // 2

    if user_collect[middle_item]['id'] <= middle_index and user_collect[middle_item + 1]['id'] > middle_index:
        return middle_item
    
    if user_collect[middle_item]['id'] <= middle_index and user_collect[middle_item + 1]['id'] <= middle_index and length - 1 == middle_item + 1:
        return 'l'
    elif user_collect[middle_item]['id'] <= middle_index and user_collect[middle_item + 1]['id'] <= middle_index:
        return search_middle_binnary(middle_index, middle_item, end_item, user_collect, length)

    if user_collect[middle_item]['id'] > middle_index and user_collect[middle_item + 1]['id'] > middle_index and middle_item == 0:
        return 'r'
    elif user_collect[middle_item]['id'] > middle_index and user_collect[middle_item + 1]['id'] > middle_index:
        return search_middle_binnary(middle_index, start_item, middle_item, user_collect, length)
    