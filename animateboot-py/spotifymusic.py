import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# -----------------------------------------------------------------
# 替换成你在 Spotify 开发者后台拿到的 ID 和 Secret
CLIENT_ID = '这里替换成你的_CLIENT_ID'
CLIENT_SECRET = '这里替换成你的_CLIENT_SECRET'
# -----------------------------------------------------------------

# 检查你是否填写了凭证
if CLIENT_ID == '这里替换成你的_CLIENT_ID' or CLIENT_SECRET == '这里替换成你的_CLIENT_SECRET':
    print("错误：请先在代码中填入你的 Spotify CLIENT_ID 和 CLIENT_SECRET。")
    print("请访问 developer.spotify.com/dashboard 获取。")
else:
    # 初始化
    try:
        auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        search_query = "Imagine Dragons Believer"
        search_limit = 5

        print(f"--- 正在 Spotify 搜索: '{search_query}' ---")

        # 调用搜索 API
        # type='track' 表示我们只搜索歌曲
        # 其他类型包括 'artist', 'album', 'playlist'
        results = sp.search(q=search_query, limit=search_limit, type='track')

        # 解析结果
        tracks = results.get('tracks', {}).get('items', [])

        if not tracks:
            print("没有找到匹配的歌曲。")
        else:
            for item in tracks:
                song_name = item['name']

                # 歌手 (可能是多个)
                artists = [artist['name'] for artist in item['artists']]
                artist_str = ", ".join(artists)

                album_name = item['album']['name']

                # 获取歌曲的 Spotify 网页链接
                song_url = item['external_urls']['spotify']

                # 获取歌曲的唯一 URI (在 Spotify 应用中使用的 ID)
                song_uri = item['uri']

                print(f"歌曲: {song_name}")
                print(f"歌手: {artist_str}")
                print(f"专辑: {album_name}")
                print(f"Spotify URI: {song_uri}")
                print(f"链接: {song_url}")
                print("------------------------------")

    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API 认证或请求失败: {e}")
        print("请检查你的 CLIENT_ID 和 CLIENT_SECRET 是否正确。")
    except Exception as e:
        print(f"发生未知错误: {e}")