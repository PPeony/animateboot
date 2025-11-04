import requests
import json

def search_qq_music(keyword, limit=5):
    """
    调用QQ音乐的非官方搜索API
    """

    # 这是QQ音乐的网页搜索接口
    url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"

    # 参数
    # w: 搜索关键字
    # p: 当前页码
    # n: 每页返回的结果数量
    # format: 'json' 或 'jsonp'
    params = {
        'w': keyword,
        'p': 1,
        'n': limit,
        'format': 'json'
    }

    # 伪造一个浏览器头，否则可能会被拒绝
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    print(f"--- 正在QQ音乐搜索: '{keyword}' ---")

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status() # 如果请求失败 (如 403, 404, 500) 则抛出异常

        data = response.json()

        # 检查返回的数据结构
        if data.get('code') == 0:
            song_list = data.get('data', {}).get('song', {}).get('list', [])

            if not song_list:
                print("没有找到匹配的歌曲。")
                return

            for song in song_list:
                song_name = song['songname']
                # 'songmid' 是用于构建网页链接的关键ID
                song_mid = song['songmid']
                # 'songid' 是另一个ID，有时也会用到
                song_id = song['songid']

                # 歌手 (可能是多个)
                artists = [singer['name'] for singer in song['singer']]
                artist_str = ", ".join(artists)

                album_name = song['albumname']

                # 构造歌曲的网页链接
                song_url = f"https://y.qq.com/n/ryqq/songDetail/{song_mid}"

                print(f"歌曲: {song_name}")
                print(f"歌手: {artist_str}")
                print(f"专辑: {album_name}")
                print(f"Song MID: {song_mid}") # 这是关键 ID
                print(f"链接: {song_url}")
                print("------------------------------")

        else:
            print(f"API返回错误: {data.get('message', '未知错误')}")

    except requests.exceptions.RequestException as e:
        print(f"网络请求出错: {e}")
    except json.JSONDecodeError:
        print("解析返回的JSON数据失败，可能是IP被限制或接口已更改。")
    except Exception as e:
        print(f"发生未知错误: {e}")

# --- 执行搜索 ---
search_qq_music("周杰伦 晴天")

# 搜索英文歌曲
# search_qq_music("Imagine Dragons")