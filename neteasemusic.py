from pyncm import apis

# 这是搜索功能所在的模块
# 你也可以用 EapiSearch (EAPI 接口) 或 WebapiSearch (Web API 接口)
# Cloudsearch (云搜索) 是比较常用的一个
from pyncm.apis import cloudsearch

# 搜索歌曲
search_query = "周杰伦 晴天"
search_limit = 5  # 只获取前 5 个结果

print(f"--- 正在搜索: '{search_query}' ---")

try:
    # 调用搜索 API
    # type=1 代表搜索"单曲"
    # 更多类型: 10=专辑, 100=歌手, 1000=歌单, ...
    results = cloudsearch.GetSearchResult(search_query, limit=search_limit, type=1)

    # 检查是否有 'result' 键并且 'songs' 键存在
    if 'result' in results and 'songs' in results['result']:
        songs = results['result']['songs']

        if not songs:
            print("没有找到匹配的歌曲。")

        for song in songs:
            # 获取歌曲 ID
            song_id = song['id']

            # 获取歌曲名称
            song_name = song['name']

            # 获取艺术家名字 (艺术家可能有多位)
            artist_names = [artist['name'] for artist in song['ar']]
            artist_str = ", ".join(artist_names)

            # 获取专辑名称
            album_name = song['al']['name']

            print(f"歌曲: {song_name}")
            print(f"歌手: {artist_str}")
            print(f"专辑: {album_name}")
            print(f"歌曲 ID: {song_id}")

            # 网易云音乐的网页链接
            song_url = f"https://music.163.com/#/song?id={song_id}"
            print(f"链接: {song_url}")
            print("------------------------------")

    else:
        print("搜索结果格式不正确或没有找到歌曲。")
        # print("原始返回:", results) # 取消注释以调试

except Exception as e:
    print(f"调用 API 时出错: {e}")
    print("这可能是因为 IP 受限或库已失效。")